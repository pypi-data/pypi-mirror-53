#!/usr/bin/env python

__author__ = "Patrick Godwin (patrick.godwin@ligo.org)"
__description__ = "a module for HTTP I/O utilities"

#-------------------------------------------------
### imports

import logging
from multiprocessing import Pool
import os
import shutil

from six.moves import urllib

from .. import utils


#-------------------------------------------------
### functions

def retrieve_timeseries(rootdir, jobs, routes, job_tag, num_threads=16):
    data = {route: {job: [[], []] for job in jobs} for route in routes}

    for route in routes:
        pool = Pool(num_threads)
        mapargs = [(job, job_tag, route, rootdir) for job in jobs]
        result = pool.map(retrieve_timeseries_by_job, mapargs)

        for sngl_data in result:
            data[route].update(sngl_data)

    return data


@utils.unpack
def retrieve_timeseries_by_job(job, job_tag, route, basedir):
    with open(os.path.join(job_tag, "%s_registry.txt" % job)) as f:
        url = f.readline().strip()
    data = get_url(url, route)
    time, data = data[0], data[1]

    return {job: [numpy.array(time), numpy.array(data)]}


def get_url(url, d):
    """!
    A function to pull data from @param url where @param d specifies a
    specific route.  FIXME it assumes that the routes end in .txt
    """
    f = "%s%s.txt" % (url, d)
    try:
        jobdata = urllib.request.urlopen(f).read().decode('utf-8').split("\n")
    except urllib.error.HTTPError as e:
        logging.error("%s : %s" % (f, str(e)))
        return
    except urllib.error.URLError as e:
        logging.error("%s : %s" % (f, str(e)))
        return
    data = []
    for line in jobdata:
        if line:
            data.append([float(x) for x in line.split()])
    data = numpy.array(data)
    out = []
    if data.shape != (0,):
        for i in range(data.shape[1]):
            out.append(data[:,i])
    return out
