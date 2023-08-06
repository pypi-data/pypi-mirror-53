def mergeSeriesOnTimestampRange(df_cpu, df_type):
  """
  Upsamples df_type to df_cpu.
  Example:
    Input
      df_cpu = pd.Series({'time': [1,2,3,4], 'field_1': [5,6,7,8]})
      df_type = pd.Series({'time': [1,3], 'field_2': ['a','b']})
    Returns
      pd.Series({'time': [1,2,3,4], 'field_1': [5,6,7,8], 'field_2': ['a','a','b','b']})
  """
  import numpy as np

  df_cpu['instanceType'] = None
  # assume df_type is sorted in decreasing EventTime order (very important)
  # NB: since some instances are not present in the cloudtrail (for which we append artificially the "now" type)
  #     Need to traverse the df_type matrix backwards
  for index, row_type in df_type.iterrows():
      # use row_type.name instead of row_type['EventTime']
      # check note above about needing to traverse backwards
      # df_cpu.iloc[np.where(df_cpu.Timestamp >= row_type.name)[0], df_cpu.columns.get_loc('instanceType')] = row_type['instanceType']
      df_cpu.iloc[np.where(df_cpu.Timestamp <= row_type.name)[0], df_cpu.columns.get_loc('instanceType')] = row_type['instanceType']

  # fill na at beginning with back-fill
  # (artifact of cloudwatch having data at days before the creation of the instance)
  df_cpu['instanceType'] = df_cpu['instanceType'].fillna(method='backfill')
  return df_cpu







def ec2_catalog():
    import requests
    from cachecontrol import CacheControl
    from cachecontrol.caches.file_cache import FileCache

    import logging
    logger = logging.getLogger('isitfit')
    logger.debug("Downloading ec2 catalog (cached to local file)")

    # based on URL = 'http://www.ec2instances.info/instances.json'
    # URL = 's3://...csv'
    # Edit 2019-09-10 use CDN link instead of direct gitlab link
    # URL = 'https://gitlab.com/autofitcloud/www.ec2instances.info-ec2op/raw/master/www.ec2instances.info/t3b_smaller_familyL2.json'
    URL = 'https://cdn.jsdelivr.net/gh/autofitcloud/www.ec2instances.info-ec2op/www.ec2instances.info/t3b_smaller_familyL2.json'

    # cached https://cachecontrol.readthedocs.io/en/latest/
    sess = requests.session()
    cached_sess = CacheControl(sess, cache=FileCache('/tmp/isitfit_ec2info.cache'))
    r = cached_sess.request('get', URL)

    # read catalog, copy from ec2op-cli/ec2op/optimizer/cwDailyMaxMaxCpu
    import json
    j = json.dumps(r.json(), indent=4, sort_keys=True)
    from pandas import read_json
    df = read_json(j, orient='split')
    
    # Edit 2019-09-13 no need to subsample the columns at this stage
    # df = df[['API Name', 'Linux On Demand cost']]

    df = df.rename(columns={'Linux On Demand cost': 'cost_hourly'})
    # df = df.set_index('API Name') # need to use merge, not index
    return df


# copied from git-remote-aws
def mysetlocale():
  li = 'en_US.utf8'
  import os
  os.environ["LC_ALL"] = li
  os.environ["LANG"]   = li




MAX_ROWS = 10
MAX_COLS = 5
MAX_STRING = 20
def display_df(title, df, csv_fn, shape, logger):
    # https://pypi.org/project/termcolor/
    from termcolor import colored

    logger.info("")

    if shape[0]==0:
      logger.info(title)
      logger.info(colored("None", "red"))
      return

    if csv_fn is not None:
      logger.info(colored("The table '%s' was saved to the CSV file '%s'."%(title, csv_fn), "cyan"))
      logger.info(colored("It could be opened in the terminal with visidata (http://visidata.org/)","cyan"))
      logger.info(colored("and you can close visidata by pressing 'q'","cyan"))
      open_vd = input(colored('Would you like to do so? yes/[no] ', 'cyan'))
      if open_vd.lower() == 'yes' or open_vd.lower() == 'y':
        logger.info("Opening CSV file `%s` with visidata."%csv_fn)
        from subprocess import call
        call(["vd", csv_fn])
        logger.info("Exited visidata.")
        logger.info(colored("The table '%s' was saved to the CSV file '%s'."%(title, csv_fn), "cyan"))
        return
      else:
        logger.info("Not opening visidata.")
        logger.info("To open the results with visidata, use `vd %s`."%csv_fn)


    # if not requested to open with visidata
    from tabulate import tabulate
    df_show = df.head(n=MAX_ROWS)
    df_show = df_show.applymap(lambda c: (c[:MAX_STRING]+'...' if len(c)>=MAX_STRING else c) if type(c)==str else c)

    logger.info(tabulate(df_show, headers='keys', tablefmt='psql', showindex=False))

    if (shape[0] > MAX_ROWS) or (shape[1] > MAX_COLS):
      logger.info("...")
      logger.info("(results truncated)")
      # done
      return

    # done
    return


class IsitfitError(Exception):
  pass



def prompt_upgrade(pkg_name, current_version):
  """
  check if current version is out-of-date
  https://github.com/alexmojaki/outdated

  copied from https://github.com/WhatsApp/WADebug/blob/958ac37be804cc732ae514d4872b93d19d197a5c/wadebug/cli.py#L40
  """

  from outdated import check_outdated

  is_outdated = False
  try:
    is_outdated, latest_version = check_outdated(pkg_name, current_version)
  except ValueError as error:
    # catch case of "ValueError: Version 0.10.0 is greater than the latest version on PyPI: 0.9.1"
    # This would happen on my dev machine
    if not "is greater than" in str(error):
      raise

  # is_outdated = True # FIXME for debugging
  if is_outdated:
    import click
    msg_outdated = """The current version of {pkg_name} ({current_version}) is out of date.
Run `pip3 install {pkg_name} --upgrade` 
to upgrade to the latest version ({latest_version})\n
"""
    msg_outdated = msg_outdated.format(
        pkg_name=pkg_name, current_version=current_version, latest_version=latest_version
      )
    click.secho(msg_outdated, fg="yellow")
  
  return is_outdated



def get_myuid():
  """
  Create a UUID for each installation of isitfit
  This also creates a .isitfit folder in the user's home directory
  and caches the generated UUID in a txt file for re-use
  """
  # get home
  import pathlib
  p1_home = str(pathlib.Path.home())

  # check dot folder
  import os
  p2_dot = os.path.join(p1_home, ".isitfit")
  if not os.path.exists(p2_dot):
    pathlib.Path(p2_dot).mkdir(exist_ok=True)

  # check uid file within dot folder
  p3_uidtxt = os.path.join(p2_dot, "uid.txt")
  uuid_val = None
  if not os.path.exists(p3_uidtxt):
    import uuid
    uuid_val = uuid.uuid4().hex
    with open(p3_uidtxt, 'w') as fh:
      fh.write(uuid_val)

  # if not created above, read from file
  if uuid_val is None:
    with open(p3_uidtxt, 'r') as fh:
      uuid_val = fh.read()

  return uuid_val


def ping_matomo(action_name):
  """
  Gather anonymous usage statistics
  """
  from urllib.parse import urljoin, urlencode

  # get uuid
  uuid_val = get_myuid()

  # build action url
  # https://stackoverflow.com/questions/9718541/reconstructing-absolute-urls-from-relative-urls-on-a-page#comment51058834_9718651
  from . import isitfit_version
  action_base = "https://cli.isitfit.io"
  action_url = urljoin(action_base, isitfit_version+action_name)

  # https://stackoverflow.com/a/39144239/4126114
  req_i = {
    "idsite": 2, # 2 is for cli.isitfit.io
    "rec": 1,
    "action_name": action_name,
    "uid": uuid_val,
    "url": action_url
  }
  payload = {"requests": ["?"+urlencode(req_i)]}

  # use POST instead of GET to avoid arguments showing up in the clear
  # https://developer.matomo.org/api-reference/tracking-api
  MATOMO_URL = 'https://isitfit.matomo.cloud/piwik.php'
  import requests
  try:
    response = requests.post(MATOMO_URL, json=payload)
  except requests.exceptions.ConnectionError as error:
    # just ignore the failure to connect
    # in order not to obstruct the CLI
    pass
