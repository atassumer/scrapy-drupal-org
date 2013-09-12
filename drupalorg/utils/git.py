class Git:
    def checkout_all_projects(self, major_version):
        # todo: need a persistent storage. csv results?
        pass

#
# class DepricatedClass:
#
#     def get_version(self, project, file_path):
#         if string.find(file_path, '/var/www/git') != -1:
#             command = 'git describe --tags'
#             self.go_to_project_dir('/var/www/git', project)
#             process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
#             tag = process.stdout.readline().rstrip()
#             return tag
#         else:
#             for line in open(file_path):
#                 buff = self.parse_line(line, 'version')
#                 if buff and buff != 'VERSION':
#                     return buff
