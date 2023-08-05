import eneel.load_runner as load_runner
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('project', help='The name of the project (i.e my_project for project.yml)')
    parser.add_argument('--connections', help='Optinally add the full path to connections.yml')
#    parser.add_argument('--logdir', help='For not using the default log directory')
    args = parser.parse_args()

    if not args.project:
        #logger.error("You need to supply your project name. I.e my_project to use my_project.yml")
        print("You need to supply your project name. I.e my_project to use my_project.yml")

#    if not args.connections:
#        logger.error("You need to supply a path to your connections.yml")

    else:
        project_name =  args.project
        import eneel.logger as logger
        logger = logger.get_logger(project_name)
        import eneel.printer as printer
        #        logger.info("Connections config: " + args.connections)
        printer.print_msg('')
        printer.print_msg('Running eneel ')
        printer.print_msg('')
        logger.debug("Loading project: " + project_name)
        try:
            load_runner.run_project(project_name, args.connections)
        except KeyboardInterrupt:
            print("Interupted by user")


if __name__ == '__main__':
    main()

