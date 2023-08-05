"""
Project CLI
"""

import click
import os
import shutil
import codecs


@click.group()
def cli():
    """Project Group"""
    pass


@cli.group()
def project():
    """Manage project, such as create, ..."""
    pass


PROJECT_TYPES = ['func', 'app']
VIRTUAL_ENV_NAME = 'venv'


def _get_run_dir():
    """获取当前运行目录"""
    # print('current dir:', os.getcwd())
    return os.getcwd()


def _get_project_folder_name(name, project_type):
    """获取工程文件夹名称"""
    return name + '_' + project_type


def _get_project_path(path, name, project_type):
    """获取工程目录"""
    return os.path.join(path, _get_project_folder_name(name, project_type))


def _check_path(path):
    """检查初始化path"""

    # path 末尾不能以 / 结尾
    if len(path) > 1 and path.endswith('/'):
        path = path[:-1]

    if path.startswith('.'):
        # 当path是'.'开头的确定为相对路径
        path = os.path.abspath(path)
    elif path == '':
        # 当path是''时，使用当前路径
        path = _get_run_dir()
    else:
        path = os.path.abspath(path)

    # 检查path是否有效存在和能读写
    # print('check path:', path)
    if os.path.exists(path):
        # 检查读写权限
        test_file_path = os.path.join(path, 't')
        try:
            f = open(test_file_path, 'w')
            f.close()
        except PermissionError or IOError:
            click.echo(f"Please check {path} directory r/w permission")
            return None
        else:
            # 删除测试文件
            os.remove(test_file_path)
    else:
        try:
            os.makedirs(path)
        except PermissionError or IOError:
            click.echo(f'Make directory {path} permission deny.')
            return None
        except OSError as e:
            click.echo(f'Make directory {path} occurred OS error. {e}')
            return None
    return path


def _check_project_path(path):
    """检查项目path"""

    # 检查是否存在
    if os.path.exists(path):
        file = os.path.split(path)[-1]
        if os.path.isdir(path):
            click.echo(f"same directory name {file}  already exists.")
        else:
            click.echo(f"same file name {file} already exists.")
        return False
    else:
        return True


def _get_template_path():
    """获取模板路径"""
    current_path = os.path.abspath(__file__)
    return os.path.join(os.path.dirname(os.path.dirname(current_path)), 'templates')


@project.command()
@click.option('-n', '--name', prompt='Please input project name', required=True, type=str, help='project name.')
@click.option('-t', '--type', prompt='Please input project type [0:func, 1:app]', required=True, type=click.IntRange(0, 1), help='project type.')
@click.option('-i', '--init_env', prompt='Init virtual env', type=bool, default=True, help='whether initialize virtual environment.')
@click.option('-p', '--path', prompt='Project path', default=_get_run_dir, type=str, help='project path')
def create(name, type, init_env, path):
    """Create project."""

    project_type = PROJECT_TYPES[type]
    # print(name, project_type, init_env, path, __file__)

    # 检查path是否有效
    path = _check_path(path)
    if path is None:
        return

    # 创建工程目录
    project_name = _get_project_folder_name(name, project_type)
    project_path = _get_project_path(path, name, project_type)

    # 检测当前文件夹是否存在同名文件
    if not _check_project_path(project_path):
        return

    # 创建父级目录
    os.mkdir(project_path)

    # 创建服务目录
    service_path = os.path.join(project_path, project_name)
    templates_path = _get_template_path()
    # print('service, template path:', service_path, templates_path)
    if project_type == 'app':
        shutil.copytree(templates_path, service_path)
    else:
        shutil.copytree(templates_path, service_path, ignore=shutil.ignore_patterns('config.py', 'roles.py'))

    # 修改服务文件夹名称
    service_code_template_path = os.path.join(service_path, 'service')
    service_code_path = os.path.join(service_path, name)
    try:
        os.rename(service_code_template_path, service_code_path)
    except OSError:
        click.echo(f"project name {name} conflict with templates directory name, please change your project name.")
        return

    # 修改service.py名称
    service_file_path = os.path.join(service_code_path, 'service.py')
    service_class_template = """class Service(object):
    
    name = '{0}'
    """.format(name)
    with codecs.open(service_file_path, 'a+', encoding='utf-8') as f:
        f.write(service_class_template)

    # 创建虚拟环境
    if init_env:
        import venv

        service_env_path = os.path.join(project_path, VIRTUAL_ENV_NAME)
        venv.create(service_env_path, with_pip=True)

    click.echo('Project created successfully! :-)')
