import hashlib

from flask import current_app
from flask_restplus import Namespace, Resource

import cea.plots.cache
from utils import deconstruct_parameters

api = Namespace('Dashboard', description='Dashboard plots')


LAYOUTS = ['row', 'grid']
CATEGORIES = {c.name: {'label': c.label, 'plots': [{'id': p.id(), 'name': p.name} for p in c.plots]}
              for c in cea.plots.categories.list_categories()}


def dashboard_to_dict(dashboard):
    out = dashboard.to_dict()
    for i, plot in enumerate(out['plots']):
        if plot['plot'] != 'empty':
            plot['hash'] = hashlib.md5(repr(sorted(plot.items()))).hexdigest()
            plot['title'] = dashboard.plots[i].title
    return out


@api.route('/')
class Dashboard(Resource):
    def get(self):
        """
        Get Dashboards from yaml file
        """
        config = current_app.cea_config
        plot_cache = cea.plots.cache.PlotCache(config)
        dashboards = cea.plots.read_dashboards(config, plot_cache)

        out = []
        for d in dashboards:
            out.append(dashboard_to_dict(d))

        return out


@api.route('/new')
class DashboardNew(Resource):
    def post(self):
        form = api.payload
        config = current_app.cea_config
        plot_cache = cea.plots.cache.PlotCache(config)

        if 'grid' in form['layout']:
            types = [[2] + [1] * 4, [1] * 6, [1] * 3 + [3], [2, 1] * 2]
            grid_width = types[int(form['layout'].split('-')[-1])-1]
            dashboard_index = cea.plots.new_dashboard(config, plot_cache, form['name'], 'grid',
                                                      grid_width=grid_width)
        else:
            dashboard_index = cea.plots.new_dashboard(config, plot_cache, form['name'], form['layout'])

        return {'new_dashboard_index': dashboard_index}


@api.route('/duplicate')
class DashboardDuplicate(Resource):
    def post(self):
        form = api.payload
        config = current_app.cea_config
        plot_cache = cea.plots.cache.PlotCache(config)

        dashboard_index = cea.plots.duplicate_dashboard(config, plot_cache, form['name'], form['dashboard_index'])

        return {'new_dashboard_index': dashboard_index}


@api.route('/delete/<int:dashboard_index>')
class DashboardDelete(Resource):
    def post(self, dashboard_index):
        form = api.payload
        config = current_app.cea_config
        cea.plots.delete_dashboard(config, dashboard_index)

        return {'message': 'deleted dashboard'}


@api.route('/set-scenario/<int:dashboard_index>')
class DashboardScenario(Resource):
    def post(self, dashboard_index):
        form = api.payload
        config = current_app.cea_config
        plot_cache = cea.plots.cache.PlotCache(config)
        dashboards = cea.plots.read_dashboards(config, plot_cache)

        dashboard = dashboards[dashboard_index]
        dashboard.set_scenario(form['scenario'])
        cea.plots.write_dashboards(config, dashboards)

        return {'new_dashboard_index': dashboard_index}


@api.route('/plot-categories')
class DashboardPlotCategories(Resource):
    def get(self):
        return CATEGORIES


@api.route('/plot-parameters/<int:dashboard_index>/<int:plot_index>')
class DashboardPlotParameters(Resource):
    def get(self, dashboard_index, plot_index):
        config = current_app.cea_config
        plot_cache = cea.plots.cache.PlotCache(config)
        dashboards = cea.plots.read_dashboards(config, plot_cache)

        dashboard = dashboards[dashboard_index]
        plot = dashboard.plots[plot_index]
        parameters = []
        for pname, fqname in plot.expected_parameters.items():
            parameter = config.get_parameter(fqname)
            if pname in plot.parameters:
                parameter.set(plot.parameters[pname])
            parameters.append(deconstruct_parameters(parameter))
        return parameters

    def post(self, dashboard_index, plot_index):
        form = api.payload
        config = current_app.cea_config
        plot_cache = cea.plots.cache.PlotCache(config)
        dashboards = cea.plots.read_dashboards(config, plot_cache)

        dashboard = dashboards[dashboard_index]
        plot = dashboard.plots[plot_index]
        print('route_post_plot_parameters: expected_parameters: {}'.format(plot.expected_parameters.items()))
        for pname, fqname in plot.expected_parameters.items():
            parameter = config.get_parameter(fqname)
            print('route_post_plot_parameters: fqname={fqname}, pname={pname}'.format(fqname=fqname, pname=pname))
            if isinstance(parameter, cea.config.MultiChoiceParameter):
                plot.parameters[pname] = parameter.decode(','.join(form[pname]))
            else:
                plot.parameters[pname] = parameter.decode(form[pname])
        cea.plots.write_dashboards(config, dashboards)

        return plot.parameters


@api.route('/change-plot/<int:dashboard_index>/<int:plot_index>')
class DashboardChangePlot(Resource):
    def post(self, dashboard_index, plot_index):
        form = api.payload
        config = current_app.cea_config
        plot_cache = cea.plots.cache.PlotCache(config)
        dashboards = cea.plots.read_dashboards(config, plot_cache)

        dashboard = dashboards[dashboard_index]
        dashboard.replace_plot(form['category'], form['plot_id'], plot_index)
        cea.plots.write_dashboards(config, dashboards)

        return {'category': form['category'], 'plot_id': form['plot_id'], 'index': plot_index}


@api.route('/add-plot/<int:dashboard_index>/<int:plot_index>')
class DashboardAddPlot(Resource):
    def post(self, dashboard_index, plot_index):
        form = api.payload
        config = current_app.cea_config
        plot_cache = cea.plots.cache.PlotCache(config)
        dashboards = cea.plots.read_dashboards(config, plot_cache)

        dashboard = dashboards[dashboard_index]
        dashboard.add_plot(form['category'], form['plot_id'], plot_index)
        cea.plots.write_dashboards(config, dashboards)

        return {'category': form['category'], 'plot_id': form['plot_id'], 'index': plot_index}


@api.route('/delete-plot/<int:dashboard_index>/<int:plot_index>')
class DashboardDeletePlot(Resource):
    def post(self, dashboard_index, plot_index):
        config = current_app.cea_config
        plot_cache = cea.plots.cache.PlotCache(config)
        dashboards = cea.plots.read_dashboards(config, plot_cache)

        dashboard = dashboards[dashboard_index]
        dashboard.remove_plot(plot_index)
        cea.plots.write_dashboards(config, dashboards)

        return dashboard_to_dict(dashboard)
