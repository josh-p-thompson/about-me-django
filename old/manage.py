import utils

def main(): 
    pages = utils.generate_page_list()
    utils.build(pages)

if __name__ == "__main__": 
    main()