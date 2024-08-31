from modules.config_reader import read_config
from modules.image_utils import convert_img_file_to_binary, get_picture_url_from_binary


def get_team_details():
    team_members = []
    config = read_config(config_path='static/team/team_config.yml')
    designations = ['ceo', 'cto', 'mo', 'doc', 'cfo', 'cpo', 'doo', 'dom']
    for des in designations:
        team_members.append(populate_member_info(config[des]))
    return team_members


def populate_member_info(config_parent_details):
    member = {'name': config_parent_details['name'], 'details': config_parent_details['details'],
              'bio': config_parent_details['bio'], 'place': config_parent_details['place'],
              'des': config_parent_details['designation'],
              'dp': get_picture_url_from_binary(convert_img_file_to_binary(config_parent_details['image']))}
    return member
