#!/usr/bin/env python

__author__ = "Patrick Godwin (patrick.godwin@ligo.org)"
__description__ = "a module for hdf5 I/O utilities"

#-------------------------------------------------
### imports

from collections import defaultdict
from itertools import count
import glob
import multiprocessing
import os
import shutil

import h5py
import numpy

from . import core
from .. import utils


#-------------------------------------------------
### classes

class Aggregator(object):
    """
    Handles the storing and aggregation of timeseries using hdf5 as a file backend.
    """
    def __init__(self, rootdir='.', aggdir='aggregator', num_processes=1, reduce_dt=300, reduce_across_tags=True, webdir='.', **kwargs):
        self.rootdir = rootdir
        self.aggdir = aggdir
        self.webdir = webdir

        ### reduction options
        self.reduce_dt = reduce_dt
        self.reduce_across_tags = reduce_across_tags
        self.pool = multiprocessing.Pool(num_processes)

        ### track reduced data to process
        self.last_reduce = utils.gps_now()
        self.prev_dataspan = set()

        ### set up 'latest' directory for snapshots
        core.makedir(os.path.join(self.webdir, 'snapshots', 'latest'))


    def store_and_reduce(self, measurement, data, columns, tags=None, aggregate='max'):
        """
        Stores and aggregates incoming timeseries into a series of hdf5 files in a hierarchical
        file directory structure.

        Args:
            measurement (str, required): The measurement name.
            data (dict(tuple: list), required): See below for guide/formatting.
            columns (tuple/str, required): A list of column names (not including time) to store.
            tags (tuple/str, optional): Key-value pairs in the form: tag_name, tag_value.
            aggregate (str, optional): The aggregate quantities to use in downsampling (i.e. max).

        Given N columns and M tags, data is passed in as follows:
            {(tag1, ..., tagM): [iterable(time), iterable(column1), ..., iterable(columnN)]}

        where each iterable is of the same length.

        In the case where no tags are passed in, data is instead passed in as a list:
            [iterable(time), iterable(column1), ..., iterable(columnN)]

        """
        dataspan = set()

        ### reduce by tag
        mapargs = []
        for tag_key in data.keys():
            if len(data[tag_key][0]) > 0:
                mapargs.append((self.rootdir, measurement, tag_key, tags, aggregate, data[tag_key][0], data[tag_key][1], self.prev_dataspan, 1))
        for ds in self.pool.map(reduce_by_tag, mapargs):
            dataspan.update(ds)
            self.prev_dataspan.update(ds)

        ### reduce across tags
        if self.reduce_across_tags:
            for start, end in zip(*core.job_expanse(dataspan)):
                reduce_across_tags((self.rootdir, measurement, data.keys(), tags, aggregate, start, end, 1))

        ### only reduce higher dt every last_reduce seconds
        if utils.in_new_epoch(utils.gps_now(), self.last_reduce, self.reduce_dt):
            self.last_reduce = utils.gps_now()

            ### reduce by tag
            mapargs = []
            for dt in (10, 100, 1000, 10000, 100000):
                for tag_key in data.keys():
                    if len(data[tag_key][0]) > 0:
                        mapargs.append((self.rootdir, measurement, tag_key, tags, aggregate, data[tag_key][0], data[tag_key][1], self.prev_dataspan, dt))
            self.pool.map(reduce_by_tag, mapargs)

            ### reduce across tags
            if self.reduce_across_tags:
                mapargs = []
                for dt in (10, 100, 1000, 10000, 100000):
                    for start, end in zip(*core.job_expanse(dataspan)):
                        mapargs.append((self.rootdir, measurement, data.keys(), tags, aggregate, start, end, dt))
                self.pool.map(reduce_across_tags, mapargs)

            self.prev_dataspan = dataspan.copy()


    def store_snapshot(self, measurement, data, dims, time, **attrs):
        """Stores a JSON-formatted snapshot to disk.

        Parameters
        ----------
        measurement : `str`
            the measurement name
        data : `dict`
            a mapping from a column to 1-dim data
        dims : `dict`
            a mapping from a dimension (one of x, y, z) to a column,
            either 2-dim (x, y) or 3-dim (x, y, z).
        time : `int`
            the time the snapshot was taken

        """
        core.store_snapshot(self.webdir, measurement, data, dims, time, **attrs)


class Consumer(object):
    """Queries data from hdf5.
    """
    def __init__(self, rootdir='.', aggdir='aggregator', **kwargs):
        self.rootdir = rootdir
        self.aggdir = aggdir


    def retrieve_timeseries_by_tag(self, measurement, start, end, column, tag, aggregate=None, dt=None):
        tags = set()
        series = defaultdict(lambda: defaultdict(list))
        duration = end - start
        mintime = None

        if tag == 'ifo':
            tagpath = ''
        else:
            tagpath = '/by_{}'.format(tag)

        if aggregate and dt:
            for n, partial_path in enumerate(get_partial_paths_to_aggregated_data(start, end, level = int(numpy.log10(dt)))):

                file_pattern = "%s/%s/%s%s/*/%s/%s.hdf5" % (self.rootdir, self.aggdir, partial_path, tagpath, aggregate, measurement)
                for file_ in glob.iglob(file_pattern):
                    try:
                        f = h5py.File(file_, "r")
                        _, tag_val, _, _ = file_.rsplit('/', 3)
                        tags.add(tag_val)

                        this_time = list(numpy.array(f['time']))
                        series[tag_val]['time'].extend(this_time)
                        series[tag_val][column].extend(list(numpy.array(f[column])))

                        if len(this_time) >= 1:
                            mintime = min(mintime, this_time[0]) if mintime else this_time[0]
                        f.close()

                    except IOError as e:
                        pass

                ### refuse to look back more than 2 directories and stop once you have enough data
                if n > 2 or (mintime is not None and (start - mintime) > duration):
                    break
        else:
            file_pattern = "%s/%s/%s/*/%s.hdf5" % (self.rootdir, self.aggdir, tagpath, measurement)
            for file_ in glob.iglob(file_pattern):
                try:
                    f = h5py.File(file_, "r")
                    _, tag_val, _, _ = file_.rsplit('/', 3)
                    tags.add(tag_val)

                    this_time = list(numpy.array(f['time']))
                    series[tag_val]['time'].extend(this_time)
                    series[tag_val][column].extend(list(numpy.array(f[column])))

                    f.close()

                except IOError as e:
                    pass

        tagdata = sorted(list(tags))
        datadata = []
        for tag_val in tagdata:
            series[tag_val]['time'] = numpy.array(series[tag_val]['time'])
            series[tag_val][column] = numpy.array(series[tag_val][column])

            ix = numpy.logical_and(series[tag_val]['time'] >= start, series[tag_val]['time'] < end)
            series[tag_val]['time'] = series[tag_val]['time'][ix]
            series[tag_val][column] = series[tag_val][column][ix]

            if len(series[tag_val]['time']):
                ix = numpy.argsort(series[tag_val]['time'])
                series[tag_val]['time'] = series[tag_val]['time'][ix]
                series[tag_val][column] = series[tag_val][column][ix]

            datadata.append(series[tag_val][column].tolist())

        timedata = series[tagdata[0]]['time'].tolist() ### NOTE: assume at least one tag and same number of datapoints for all tags

        return timedata, tagdata, datadata


    def retrieve_binnedtimeseries_by_tag(self, measurement, start, end, column, tag, aggregate=None, dt=None):
        if aggregate and dt:
            start = int(numpy.floor(start / dt) * dt)
            end = int(numpy.ceil(end / dt) * dt)
        duration = end - start

        if tag == 'ifo':
            tagpath = ''
        else:
            tagpath = '/by_{}'.format(tag)

        if aggregate and dt:
            for partial_path in get_partial_paths_to_aggregated_data(start, end, level = int(numpy.log10(dt))):
                tagdata = sorted([x.split("/")[-1] for x in glob.iglob("%s/%s/%s%s/*" % (self.rootdir, self.aggdir, partial_path, tagpath))])
                break

            timedata = (numpy.arange((end-start)/dt+1)*dt + start).astype(int)
        else:
            tagdata = sorted([x.split("/")[-1] for x in glob.iglob("%s/%s/%s/*" % (self.rootdir, self.aggdir, tagpath))])
            timedata = (numpy.arange(duration) + start).astype(int)

        datadata = numpy.zeros((len(tagdata), len(timedata)), dtype="double") + float("nan")

        if aggregate and dt:
            for n, partial_path in enumerate(get_partial_paths_to_aggregated_data(start, end, level = int(numpy.log10(dt)))):

                for i, tag in enumerate(tagdata):
                    file_ = "%s/%s/%s%s/%s/%s/%s.hdf5" % (self.rootdir, self.aggdir, partial_path, tagpath, tag, aggregate, measurement)
                    try:
                        #print file_
                        f = h5py.File(file_, "r")
                        this_time = numpy.array(f['time'])
                        this_data = numpy.array(f['data'])
                        tix = numpy.logical_and(this_time >= start, this_time < end)
                        this_time = this_time[tix]
                        this_data = this_data[tix]
                        if len(this_time) > 0:
                            ix = numpy.digitize(this_time, timedata)
                            datadata[i,ix] = this_data
                        f.close()

                    except IOError as e:
                        pass
        else:
            for i, tag in enumerate(tagdata):
                file_ = "%s/%s/%s/%s/%s.hdf5" % (self.rootdir, self.aggdir, tagpath, tag, measurement)
                try:
                    #print file_
                    f = h5py.File(file_, "r")
                    this_time = numpy.array(f['time'])
                    this_data = numpy.array(f['data'])
                    tix = numpy.logical_and(this_time >= start, this_time < end)
                    this_time = this_time[tix]
                    this_data = this_data[tix]
                    if len(this_time) > 0:
                        ix = numpy.digitize(this_time, timedata)
                        datadata[i,ix] = this_data
                    f.close()

                except IOError as e:
                    pass

        return timedata.tolist(), tagdata, datadata.tolist()


    def retrieve_timeseries(self, measurement, start, end, column, tags=None, aggregate=None, dt=None):
        this_data = numpy.empty((0))
        this_time = numpy.empty((0))
        mintime = None
        duration = end - start

        ### NOTE: only handles job, ifo tags for now
        tagpath = ''
        if tags:
            for tag, val in tags:
                if tag == 'ifo':
                    measurement = '{}_{}'.format(val, measurement)
                else:
                    tagpath = '/by_{}/{}'.format(tag, val)

        if aggregate and dt:
            for n, partial_path in enumerate(get_partial_paths_to_aggregated_data(start, end, int(numpy.log10(dt)))):
                try:
                    fname = "%s/%s/%s%s/%s/%s.hdf5" % (self.rootdir, self.aggdir, partial_path, tagpath, aggregate, measurement)
                    f = h5py.File(fname, "r")
                    this_data = numpy.hstack((numpy.array(f[column]), this_data))
                    this_time = numpy.hstack((numpy.array(f['time']), this_time))

                    if len(this_time) >= 1:
                        mintime = min(mintime, this_time[0]) if mintime else this_time[0]
                    f.close()

                except IOError as e:
                    pass
                ### refuse to look back more than 2 directories and stop once you have enough data
                if n > 2 or (mintime is not None and (start - mintime) > duration):
                    break
        else:
            try:
                fname = "%s/%s/%s/%s.hdf5" % (self.rootdir, self.aggdir, tagpath, measurement)
                f = h5py.File(fname, "r")
                this_data = numpy.hstack((numpy.array(f[column]), this_data))
                this_time = numpy.hstack((numpy.array(f['time']), this_time))
                f.close()

            except IOError as e:
                pass

        ix = numpy.logical_and(this_time >= start, this_time < end)
        this_time = this_time[ix]
        this_data = this_data[ix]

        ix = numpy.argsort(this_time)
        return this_time[ix].tolist(), this_data[ix].tolist()


    def retrieve_ndim_latest(self, measurement, start, end, columns, tags=None):
        tagpath = ''
        if tags:
            for tag, val in tags:
                if tag == 'ifo':
                    measurement = '{}-{}'.format(val, measurement)
                else:
                    tagpath = '/by_{}/{}'.format(tag, val)

        ### retrieve all ndim files, sorted by latest
        ndim_files = []
        for partial_path in get_partial_paths_to_aggregated_data(start, end, 0):
            glob_pattern = "%s/%s/%s%s/%s-*-*.hdf5" % (self.rootdir, self.aggdir, partial_path, tagpath, measurement)
            ndim_files.extend(glob.glob(glob_pattern))
        ndim_files.sort(reverse=True)
        ndim_files = [ndfile for ndfile in ndim_files if file_in_range(ndfile, start, end)]

        if ndim_files:
            with h5py.File(ndim_files[0], "r") as f:
                return float(numpy.array(f['time'])), {col: numpy.array(f[col]).tolist() for col in columns}
        else:
            return None, {col: [] for col in columns}


#-------------------------------------------------
### reduction utilities

def store_timeseries(path, route, time, data):
    core.makedir(path)
    tmpfname, fname = create_new_dataset(path, route, time, data, tmp = True)
    # FIXME don't assume we can get the non temp file name this way
    shutil.move(tmpfname, fname)


@utils.unpack
def reduce_by_tag(rootdir, route, tag, tag_type, aggregate, time, data, prevdataspan, dt):
    if tag_type == 'ifo':
        route = '{}_{}'.format(tag, route)
    func = core.aggregate_to_func(aggregate)

    dataspan = set()
    gps1, gps2 = core.gps_range(time)

    for start, end in zip(gps1, gps2):
        # shortcut to not reprocess data that has already been
        # processed.  Dataspan was the only thing that was
        # previously determined to be needing to be updated
        # anything before that is pointless
        if prevdataspan and end < min(prevdataspan):
            continue

        if dt == 1:
            for processed_time in update_lowest_level(rootdir, route, tag, tag_type, start, end, aggregate, func, numpy.array(time), numpy.array(data)):
                dataspan.add(processed_time)

        else:
            level = numpy.log10(dt).astype(int)
            reduce_by_one_level(rootdir, route, tag, tag_type, start, end, aggregate, func, level)

    return dataspan


@utils.unpack
def reduce_across_tags(rootdir, route, tags, tag_type, aggregate, start, end, dt):
    level = numpy.log10(dt).astype(int)
    func = core.aggregate_to_func(aggregate)

    setup_dir_across_tag_by_level(start, aggregate, route, rootdir, verbose = True, level=level)
    agg_time = numpy.array([])
    agg_data = numpy.array([])
    for tag in sorted(tags):
        path = path_by_tag(rootdir, tag, tag_type, start, end, aggregate, level=level)
        agg_time, agg_data = aggregate_data(path, route, agg_time, agg_data)

    _, reduced_time, reduced_data = core.reduce_data(agg_time, agg_data, func, dt=dt)

    path = path_across_tags(rootdir, start, end, aggregate, level=level)
    store_timeseries(path, route, reduced_time, reduced_data)


def update_lowest_level(rootdir, route, tag, tag_type, start, end, typ, func, jobtime, jobdata):
    path = path_by_tag(rootdir, tag, tag_type, start, end, typ)
    try:
        fname, prev_times, prev_data = get_dataset(path, route)
    except:
        setup_dir_by_tag_and_level(start, typ, tag, tag_type, route, rootdir, verbose = True, level = 0)
        fname, prev_times, prev_data = get_dataset(path, route)

    # only get new data and assume that everything is time ordered
    if prev_times.size:
        this_time_ix = numpy.logical_and(jobtime > max(start-1e-16, prev_times[-1]), jobtime < end)
    else:
        this_time_ix = numpy.logical_and(jobtime >= start, jobtime < end)

    this_time = numpy.concatenate((jobtime[this_time_ix], prev_times))
    this_data = numpy.concatenate((jobdata[this_time_ix], prev_data))

    # shortcut if there are no updates
    if len(this_time) == len(prev_times) and len(this_data) == len(prev_data):
        return []
    else:
        _, reduced_time, reduced_data = core.reduce_data(this_time, this_data, func, dt=1)
        store_timeseries(path, route, reduced_time, reduced_data)
        return [start, end]


def reduce_by_one_level(rootdir, route, tag, tag_type, start, end, typ, func, level):
    agg_data = numpy.array([])
    agg_time = numpy.array([])

    # FIXME iterate over levels instead.
    this_level_dir = "/".join([rootdir, core.gps_to_leaf_directory(start, level = level)])
    for subdir in gps_to_sub_directories(start, level, rootdir):
        if tag_type == 'ifo':
            path = "/".join([this_level_dir, subdir, typ])
        else:
            path = "/".join([this_level_dir, subdir, "by_{}".format(tag_type), tag, typ])
        agg_time, agg_data = aggregate_data(path, route, agg_time, agg_data)

    _, reduced_time, reduced_data = core.reduce_data(agg_time, agg_data, func, dt=10**level)
    path = path_by_tag(rootdir, tag, tag_type, start, end, typ, level=level)
    store_timeseries(path, route, reduced_time, reduced_data)


def aggregate_data(path, route, agg_time, agg_data):
    try:
        _, time, data = get_dataset(path, route)
        agg_time = numpy.concatenate((agg_time, time))
        agg_data = numpy.concatenate((agg_data, data))
    except IOError as ioerr:
        core.makedir(path)
        create_new_dataset(path, route)
        pass

    return agg_time, agg_data


#-------------------------------------------------
### misc utilities

def file_in_range(filename, start, end):
    basename = os.path.splitext(os.path.basename(filename))[0]
    _, file_start, file_duration = basename.rsplit('-', 2)
    file_start = int(file_start)
    file_end = file_start + int(file_duration)
    return file_start >= start and file_end <= end


def path_by_tag(rootdir, tag, tag_type, start, end, typ, level=0):
    if tag_type == 'ifo':
        return "/".join([rootdir, core.gps_to_leaf_directory(start, level=level), typ])
    else:
        return "/".join([rootdir, core.gps_to_leaf_directory(start, level=level), "by_{}".format(tag_type), tag, typ])


def path_across_tags(rootdir, start, end, typ, level=0):
    return "/".join([rootdir, core.gps_to_leaf_directory(start, level=level), typ])


def get_partial_paths_to_aggregated_data(start, end, level=0):
    for n in count():
        this_time = start + n * (10**level * core.MIN_TIME_QUANTA)
        if this_time <= end:
            yield core.gps_to_leaf_directory(this_time, level)
        else:
            break


def gps_to_sub_directories(gpstime, level, basedir):
    """!
    return the entire relevant directory structure for a given GPS time
    """
    root = os.path.join(basedir, core.gps_to_leaf_directory(gpstime, level))
    out = []
    for i in range(10):
        path = os.path.join(root,str(i))
        if os.path.exists(path):
            out.append(str(i))
    return out


def setup_dir_by_tag_and_level(gpstime, typ, tag, tag_type, route, rootdir, verbose = True, level = 0):
    """!
    Given a gps time, the tag and data types produce an
    appropriate data structure for storing the hierarchical data.
    """
    str_time = str(gpstime).split(".")[0]
    str_time = str_time[:(len(str_time)-int(numpy.log10(core.MIN_TIME_QUANTA))-level)]
    if tag_type == 'ifo':
        directory = "%s/%s/%s" % (rootdir, "/".join(str_time), typ)
    else:
        directory = "%s/%s/by_%s/%s/%s" % (rootdir, "/".join(str_time), tag_type, tag, typ)
    core.makedir(directory)
    tmpfname, fname = create_new_dataset(directory, route)


def setup_dir_across_tag_by_level(gpstime, typ, route, rootdir, verbose = True, level = 0):
    """!
    Given a gps time and data types produce an
    appropriate data structure for storing the hierarchical data.
    """
    str_time = str(gpstime).split(".")[0]
    str_time = str_time[:(len(str_time)-int(numpy.log10(core.MIN_TIME_QUANTA))-level)]
    directory = "%s/%s/%s" % (rootdir, "/".join(str_time), typ)
    core.makedir(directory)
    tmpfname, fname = create_new_dataset(directory, route)


def create_new_dataset(path, base, timedata = None, data = None, tmp = False):
    """!
    A function to create a new dataset with time @param timedata and data
    @param data.  The data will be stored in an hdf5 file at path @param path with
    base name @param base.  You can also make a temporary file.
    """
    tmpfname = "/dev/shm/%s_%s" % (path.replace("/","_"), "%s.hdf5.tmp" % base)
    fname = os.path.join(path, "%s.hdf5" % base)
    if not tmp and os.path.exists(fname):
        return tmpfname, fname
    f = h5py.File(tmpfname if tmp else fname, "w")
    if timedata is None and data is None:
        f.create_dataset("time", (0,), dtype="f8")
        f.create_dataset("data", (0,), dtype="f8")
    else:
        if len(timedata) != len(data):
            raise ValueError("time data %d data %d" % (len(timedata), len(data)))
        f.create_dataset("time", (len(timedata),), dtype="f8")
        f.create_dataset("data", (len(data),), dtype="f8")
        f["time"][...] = timedata
        f["data"][...] = data

    f.close()
    return tmpfname, fname


def get_dataset(path, base):
    """!
    open a dataset at @param path with name @param base and return the data
    """
    fname = os.path.join(path, "%s.hdf5" % base)
    try:
        f = h5py.File(fname, "r")
        x,y = numpy.array(f["time"]), numpy.array(f["data"])
        f.close()
        return fname, x,y
    except IOError:
        tmpfname, fname = create_new_dataset(path, base, timedata = None, data = None, tmp = False)
        return fname, numpy.array([]), numpy.array([])
