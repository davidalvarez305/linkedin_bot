import sys
from pkg.bot import Bot
from dotenv import load_dotenv

def main():
    load_dotenv()
    if "-k" in sys.argv:
        index = sys.argv.index("-k")
        
        if len(sys.argv) > index + 1:
            string_arg = " ".join(sys.argv[index + 1:])
            
            bot = Bot(string_arg)
            bot.crawl_jobs()
        else:
            raise Exception("No string argument provided after the -k flag.")
    else:
        raise Exception("The -k flag is not specified.")

if __name__ == "__main__":
    main()