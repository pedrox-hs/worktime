#!/usr/bin/env python3
"""Calculate total hours and total amount in BRL (R$) of a Trello board."""

import argparse
import os
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


def main():
  args = read_args()
  df = parse_csv(args.paths, args.member, args.hour_price)
  print(df)


def parse_csv(paths: list[str], member: str, hour_price: float):
  """Parse CSV files and calculate total hours and total amount in BRL (R$)."""
  dfs = [pd.read_csv(sheet_path, sep=',', header=0) for sheet_path in paths]
  df = pd.concat(dfs, ignore_index=True)

  df = df.drop('Card title', axis=1)
  df = df.drop('Card labels', axis=1)
  df = df.drop('Time (formatted)', axis=1)

  df['Member name(s)'] = df['Member name(s)'].str.extract(r'\((.*?)\)')
  df = df[df['Member name(s)'] == member]

  df['Start datetime'] = pd.to_datetime(df['Start datetime'])
  df['End datetime'] = pd.to_datetime(df['End datetime'])
  df['Duration'] = df['Time (seconds)']

  df = df.groupby([df['Start datetime'].dt.strftime('%Y-%m')])['Duration'].sum()

  df.index.name = 'Month'
  df = df.sort_index(ascending=False)

  df = df.to_frame().assign(Total=lambda x: x['Duration'] / 3600 * hour_price)
  df['Duration'] = df['Duration'].div(3600)
  df['Duration'] = df['Duration'].round(2)
  df.loc['Total'] = df.sum()

  # format Duration (hours) to duration format (e.g. 1h30m)
  df['Duration'] = df['Duration'].map(lambda x: f'{int(x)}h{int(x % 1 * 60)}m')

  # format Total to BRL (R$)
  df['Total'] = df['Total'].map('R$ {:,.2f}'.format) # pylint: disable=consider-using-f-string

  df = df.rename(columns={'Total': 'Total (BRL)'})

  return df


def read_args():
    """Read arguments from command line."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
      '--hour-price',
      dest='hour_price',
      type=float,
      default=os.environ['HOUR_PRICE'],
      help='hour price in BRL (R$)',
    )
    parser.add_argument(
      '--member',
      dest='member',
      type=str,
      default=os.environ['MEMBER'],
      help='member name',
    )
    parser.add_argument(
      'paths',
      type=path,
      nargs='+',
      help='path to the CSV file',
    )

    return parser.parse_args()


def path(path: str) -> str:
    """Check if path exists."""
    full_path = str(Path(path).resolve()) 
    if not os.path.exists(full_path):
        raise argparse.ArgumentTypeError(f'Path {full_path} does not exist.')
    return full_path


if __name__ == '__main__':
    main()
