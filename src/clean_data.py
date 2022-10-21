import pandas as pd

# plot missing data


# deal with missing data

# plot all features to see if they're worth keeping

# deal with the 0 relationships issue

def main():

    # put data into dataframe
    with open("data/wdw_data.csv") as f:
        data = pd.read_csv(f)
    
    print(data.head())

if __name__ == "__main__":
    main()