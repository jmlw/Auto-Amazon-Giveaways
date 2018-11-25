import asyncio
import argparse
from lib.giveaway import GiveAwayBot

async def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--user", help="email address for Amazon")
    parser.add_argument("-p", "--password", help="password for Amazon")
    args = parser.parse_args()
    
    email = None
    password = None
    if args.user:
        email = args.user
    if args.password:
        password = args.password

    ga_bot = GiveAwayBot(email=email, password=password)
    # first ga page
    ga_page = await ga_bot.login()
    # recursive function to repeat bot tasks for every ga page
    async def do_ga_workflow(page):
        last_page = await ga_bot.check_for_last_page(page)
        while last_page is False:
            await ga_bot.process_giveaways(page)
            next_page = await ga_bot.iterate_page(page)
            await do_ga_workflow(next_page)
        await ga_bot.no_req_giveaways()
    # call recursive function to process all bot tasks.
    await do_ga_workflow(ga_page)

asyncio.get_event_loop().run_until_complete(main())
