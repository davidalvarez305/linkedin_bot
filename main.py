import argparse
from pkg.bot import Bot
from dotenv import load_dotenv

def main():
    load_dotenv()

    # Create an argument parser
    parser = argparse.ArgumentParser()

    # Initialize bot
    bot = Bot()

    # Add the -c and -a flags
    parser.add_argument('-c', action='store_true', help='Call crawl_jobs() method')
    parser.add_argument('-a', action='store_true', help='Call apply_to_jobs() method')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check which flag was provided
    if args.c:
        bot.get_keywords()
        for keyword in bot.keywords:
            bot.crawl_jobs(keyword)
            pass
    elif args.a:
        bot.apply_to_jobs()
    else:
        raise Exception("No flag provided. Please use either -c or -a.")

if __name__ == "__main__":
    main()