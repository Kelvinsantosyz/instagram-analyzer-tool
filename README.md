# Instagram Analyzer Tool

This project is an Instagram analyzer tool that allows you to extract information about a user's posts, such as engagement rate, likes, comments, and comments' authors. It provides two ways to visualize the data: a graph that displays the engagement rate over time and a dataframe that contains information about the posts.

## Installation

To use this tool, you need to have Python 3 and the Instaloader library installed. You can install Instaloader using pip:

```
pip install instaloader
```

You also need to install the following libraries:
```
datetime
matplotlib
pandas
```

## How to Use

1. Clone this repository or download the files.
2. Open the `config.py` file and set your Instagram credentials.
3. Import the classes you want to use in your Python script.
4. Create an instance of the class, passing the necessary arguments.
5. Call the method of the class you want to use.

### Example

```python
from instagram_analyzer_graph import InstagramAnalyzerGraph

# Create an instance of the InstagramAnalyzerGraph class
analyzer_graph = InstagramAnalyzerGraph("your_username", "your_password", "target_profile")

# Login to Instagram
analyzer_graph.login()

# Plot a graph of the last 10 posts
max_posts = 10
analyzer_graph.plot_graph(max_posts=max_posts)
```

## Classes


### InstagramAnalyzerGraph

This class extends the `InstagramAnalyzerTool` class and adds a method to plot a graph of the engagement rate over time.

### InstagramAnalyzerDF

This class extends the `InstagramAnalyzerTool` class and adds a method to get a dataframe containing information about the posts.

### InstagramAnalyzerLikes

This class extends the `InstagramAnalyzerTool` class and adds a method to get a list of usernames who have liked the posts.

