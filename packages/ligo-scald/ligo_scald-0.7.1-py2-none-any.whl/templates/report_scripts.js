%import json
<script>
  var app = new Vue({
    el: '#report',
    data: function () {
      return {
        totalRows: {},
        perPage: 10,
        currentPage: {},
        fields: {},
        items: {},
        plotdata: {},
        plotopts: {},
	plotdataopts: {},
        plotlayout: {}
      }
    },
    methods: {
      getTableJson: function (url) {
        axios
          .get(url)
          .then(response => {
            Vue.set(this.items, url, response.data.items);
            Vue.set(this.fields, url, response.data.fields);
            Vue.set(this.totalRows, url, response.data.items.length);
            Vue.set(this.currentPage, url, 1);
          })
      },
      getPlotJson: function (url, div, layout, options, data_options) {
        axios
          .get(url)
          .then(response => {
            Vue.set(this.plotdata, url, response.data);
            Vue.set(this.plotopts, url, options);
	    Vue.set(this.plotdataopts, url, data_options);
            Vue.set(this.plotlayout, url, layout);
            return response.data;
          })
          .then(data => {
	    var trace = add_data_options(this.plotdata[url], this.plotdataopts[url])
            Plotly.react(div, trace, this.plotlayout[url], this.plotopts[url]);
          })
      }
    },
    delimiters: ['[[',']]'],
  });

% for i, c in enumerate(content):
%    if c['name'] == 'table':
       app.getTableJson('{{ c['url'] }}');
%    elif c['name'] == 'plot':
%      div_suffix = c['title'].lower().replace(' ', '_').replace(':','').replace('.', '')
       app.getPlotJson('{{ c['url'] }}', 'plot_{{ div_suffix }}', {{! json.dumps(c['layout'])  }}, {{! json.dumps(c['options']) }}, {{! json.dumps(c['data_options']) }});
%    end
% end
</script>
