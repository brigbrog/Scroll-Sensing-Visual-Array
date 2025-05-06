import os
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def total_scroll_time(df):
    # diff between first and last timestamp
    return df['time_sec'].iloc[-1] - df['time_sec'].iloc[0]

def num_scrolls(df):
    # number of non-zero scroll frequencies
    return df[df['scroll_freq'] > 0].shape[0]

def time_between_scrolls(df):
    # time between scrolls
    df['time_diff'] = df['time_sec'].diff()
    # remove null rows
    return df['time_diff'].dropna()

def scroll_interval_regularity(df):
    # how consistent the time between scrolls is
    # lower std = more regular scroll intervals
    time_diffs = time_between_scrolls(df)
    return time_diffs.std()

def plot_scroll_frequency(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['time_sec'], df['scroll_freq'], label='Scroll Frequency')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Scroll Frequency')
    plt.title('Scroll Frequency Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_interval_histogram(df):
    time_diffs = time_between_scrolls(df)
    plt.figure(figsize=(10, 6))
    plt.hist(time_diffs, bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel('Time Between Scrolls (seconds)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Time Between Scrolls')
    plt.grid(True)
    plt.show()

def analyze_participant(file_path):
    df = load_data(file_path)

    total_time = total_scroll_time(df)
    num_scrolls_val = num_scrolls(df)
    time_diff = time_between_scrolls(df)
    regularity = scroll_interval_regularity(df)

    print(f"Total scroll time: {total_time:.2f} seconds")
    print(f"Number of scrolls: {num_scrolls_val}")
    print(f"Average time between scrolls: {time_diff}")
    print(f"Regularity: {regularity:.2f} seconds")

    plot_scroll_frequency(df)
    plot_interval_histogram(df)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, ".../raw")
EDITED_DIR = os.path.join(SCRIPT_DIR, ".../edited")
P1_FILE = os.path.join(EDITED_DIR, "p1.csv")
analyze_participant(P1_FILE)
