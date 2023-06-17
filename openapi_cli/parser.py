import argparse

import six

urlparse = six.moves.urllib.parse


def parse_args(specs):
    main_parser = ArgumentParser(add_help=True)
    main_container = main_parser.add_subparsers(help='API entry points')
    main_container.required = True

    setup_parser = main_container.add_parser('mngmt', help='OpenAPI-CLI management commands')
    setup_parser.add_argument(
        '--invalidate-cache',
        help='Invalidate OpenAPI-CLI caches',
        action='store_true',
        dest='invalidate_cache',
        required=True,
    )

    base_path_map = {}
    for spec in specs:
        base_path = spec.get('basePath', '/')
        endpoints = spec['paths']
        tags = {tag['name']: tag['description'] for tag in spec.get('tags', [])}

        entities = {}
        for endpoint, endpoint_spec in endpoints.items():
            parsed_endpoint = (
                tuple() if endpoint == '/'
                else tuple(endpoint.split('/'))[1:]
            )
            base_path_map[parsed_endpoint] = base_path

            container = main_container
            for item_id, item in enumerate(parsed_endpoint):
                container.dest = 'chain.i{}'.format(item_id)
                entity_name = parsed_endpoint[:item_id + 1]
                entity = entities.get(entity_name)
                if entity:
                    container = entity
                else:
                    parser = container.add_parser(item, help=item)
                    container = parser.add_subparsers(
                        title='{} subcommands'.format(item),
                        description=None,
                        help='Item description:',
                    )
                    container.required = True
                    entities[entity_name] = container

            container.dest = 'method'

            for method, method_spec in endpoint_spec.items():
                parser = container.add_parser(method, help=method_spec.get('summary'))
                group = parser.add_argument_group('kwargs')
                for param in method_spec.get('parameters', []):
                    group.add_argument(
                        '--{}'.format(param['name']),
                        help=param.get('description'),
                        required=param.get('required', False),
                        dest='kwargs.{}'.format(param['name'])
                    )

    args = main_parser.parse_args(namespace=Namespace())
    endpoint = (
        tuple()
        if not hasattr(args, 'chain') or getattr(args.chain, 'i0', None) is None
        else tuple(name for i, name in sorted(vars(args.chain).items()))
    )
    base_path = base_path_map.get(endpoint, '')

    if base_path:
        args.path = urlparse.urljoin(base_path, '/'.join(endpoint))
    else:
        # workaround to set correct method for / endpoint (i.e. if no endpoint path supplied)
        args.path = '/'

    return args


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self.add_argument(
            '--dry-run',
            help='',
            dest='dry_run',
            action='store_true'
        )
        self.add_argument(
            '--debug',
            help='Enable debug logging',
            dest='debug',
            action='store_true'
        )
        self.add_argument(
            '--color',
            help='Enable color output',
            dest='color',
            action='store_true'
        )


class Namespace(argparse.Namespace):
    def __setattr__(self, name, value):
        if '.' in name:
            group, name = name.split('.', 1)
            namespace = getattr(self, group, Namespace())
            setattr(namespace, name, value)
            self.__dict__[group] = namespace
        else:
            self.__dict__[name] = value
