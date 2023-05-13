import instaloader
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


class InstagramAnalyzerTool:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.L = instaloader.Instaloader()
        self.posts_engagement = []
        self.posts_dates = []
        


    def login(self):
        try:
            self.L.context.log("Logging in...")
            self.L.context.login(self.username, self.password)
        except instaloader.exceptions.ConnectionException as e:
            raise Exception(f"Error: Login failed. {e}")
        except instaloader.exceptions.InvalidArgumentException:
            raise Exception("Error: Invalid username or password.")
        except instaloader.exceptions.BadResponseException as e:
            raise Exception(f"Error: Login failed. {e}")
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            raise Exception("Two-factor authentication is required.")

        # Two-factor authentication
        if self.L.context.is_logged_in:
            return True
        else:
            two_factor_code = input("Please enter your two-factor authentication code: ")
            try:
                self.L.context.two_factor_login(two_factor_code)
                print("Two-factor authentication successful.")
                return True
            except instaloader.exceptions.TwoFactorAuthRequiredException:
                raise Exception("Error: Invalid two-factor authentication code.")    
                
    def get_profile(self, target_profile):
        try:
            self.profile = instaloader.Profile.from_username(self.L.context, target_profile)
        except instaloader.exceptions.ProfileNotExistsException:
            raise Exception("Error: Profile not found. Please verify the profile name and try again.")
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            raise Exception("Error: This is a private profile and you are not following it.")

            
    def analyze_posts(self, max_posts):
        count = 0
        for post in self.profile.get_posts():
            if count >= max_posts:
                break
            count += 1
            likes_count = post.likes
            comments_count = post.comments
            followers_count = self.profile.followers
            engagement_rate = (likes_count + comments_count) / followers_count * 100
            self.posts_engagement.append(engagement_rate)
            date_posted = post.date_local.strftime('%Y-%m-%d %H:%M:%S')
            self.posts_dates.append(datetime.strptime(date_posted, '%Y-%m-%d %H:%M:%S'))
            
            
class InstagramAnalyzerGraph(InstagramAnalyzerTool):
    def __init__(self, username, password, target_profile):
        super().__init__(username, password)
        self.get_profile(target_profile)
        self.posts_engagement = []
        self.posts_dates = []
        
    def plot_graph(self, max_posts):
        """
        Plots a graph of engagement rate for the specified number of recent posts.
        """
        self.analyze_posts(max_posts)
        plt.style.use('ggplot')
        plt.figure(figsize=(12, 6))
        plt.plot(self.posts_dates, self.posts_engagement)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(["Engagement"], loc="upper left")
        plt.title(f"Engagement of the last {max_posts} posts from {self.profile.username}")
        plt.xlabel("Date")
        plt.ylabel("Engagement Rate (%)")
        plt.show()

class InstagramAnalyzerDF(InstagramAnalyzerTool):
    def __init__(self, username, password, target_profile):
        super().__init__(username, password)
        self.get_profile(target_profile)

    def get_posts_df(self, max_posts):
        """
        Returns a pandas dataframe containing information about the specified number of recent posts.
        """
        posts_data = []
        count = 0
        for post in self.profile.get_posts():
            if max_posts and count >= max_posts:
                break
            count += 1
            post_data = {
                'shortcode': post.shortcode,
                'upload_date': post.date_local,
                'likes': post.likes,
                'comments': post.comments,
                'caption': post.caption,
            }
            posts_data.append(post_data)
        posts_df = pd.DataFrame(posts_data)
        return posts_df


class InstagramAnalyzerLikes(InstagramAnalyzerTool):
    def __init__(self, username, password, target_profile):
        super().__init__(username, password)
        self.get_profile(target_profile)

    def get_likes(self, max_posts):
        """
        Returns a list of usernames who have liked the specified number of recent posts.
        """
        likes = []
        count = 0
        for post in self.profile.get_posts():
            if max_posts and count >= max_posts:
                break
            count += 1
            for like in post.get_likes():
                likes.append(like.username)
        return likes


    

# Using the InstagramAnalyzerLikes class to get information about likes


analyzer_likes = InstagramAnalyzerLikes("your_username", "your_password", "target_profile")
analyzer_likes.login()
max_posts = 10
likes = analyzer_likes.get_likes(max_posts)
print(likes)

# Using the InstagramAnalyzerDF class to get information about posts in a DataFrame
analyzer_df = InstagramAnalyzerDF("your_username", "your_password")
analyzer_df.login()
max_posts = 10
df = analyzer_df.get_posts_df(max_posts=max_posts)
print(df)

# Using the InstagramAnalyzerGraph class to generate a graph of likes and comments for a profile
analyzer_graph = InstagramAnalyzerGraph("your_username", "your_password", "target_profile")
analyzer_graph.login()
max_posts = 10
analyzer_graph.plot_graph(max_posts=max_posts)
