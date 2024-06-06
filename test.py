import spam

if __name__ == '__main__':
    print(spam.searchLogSize())
    print(spam.viewLogSize())

    spam.logSearch('컴퓨터', 'Title')
    spam.logSearch('게임', 'Title')

    print(spam.searchLogSize())
    print(spam.getSearchLog(0))
    print(spam.getSearchLog(1))