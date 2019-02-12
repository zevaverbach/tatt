import config


def print_all_services(free_only=False, print_=True):
    # TODO: make a jinja template for this
    all_services_string = (
         '\n\nHere are all the available ' +
         f'{"free " if free_only else ""}speech-to-text services:' +
        '\n\n' +
        '\n'.join(['{}{}{}{}'.format('\t', service_name, '\t\t',

                       f'({info["free"].replace("_", " ")})' 
                       if isinstance(info["free"], str) else ""
                       
                                      )

                     for service_name, info in
                     config.STT_SERVICES.items()])
        + '\n'
    )
    if print_:
        print(all_services_string)
    return all_services_string
