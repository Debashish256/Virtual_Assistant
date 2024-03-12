from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# speech Engine initialisation
engine = pyttsx3.init()
# get the voice property
voice = engine.getProperty("voice")
# set the voice property
engine.setProperty("voice", voice[1])  # 0 for male  1 for female
# an wakeuo word
activationWord = "computer"

# selecting the browser
# set the path for the browser
bravePath = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
# register the browser to the web browser so that you can choose later
webbrowser.register("brave", None, webbrowser.BackgroundBrowser(bravePath))

# get the Wolframaplha appid
appId = "LG83QG-LUYGLTUR6L"
# activating the wolframaplha id
wolframClient = wolframalpha.Client(appId)


# function for speaking
def speakUp(text: object, rate: object = 160) -> object:  # rate at which the AI will say
    engine.setProperty("rate", rate)
    # make the AI speak
    engine.say(text)
    # make it waits
    engine.runAndWait()


# create a function for getting the command
def takeCommand():
    # activate the speech recogniser
    listener = sr.Recognizer()
    print("What's NOW???????")

    # setup the system microphone
    with sr.Microphone() as source:
        # time before it stop listesing after i speakuo
        listener.pause_threshold = 2
        # get the info from the microphone
        inputSpeech = listener.listen(source)

    # recognizing the user
    try:
        print("Hoping i know you :<)")
        query = listener.recognize_google(inputSpeech, language="en_gb")
        print(f'So this is what you said-- {query}')
        # speakUp("I Know you.")

    # if the speaker is not recognized
    except Exception as exception:
        print("Wait a minute.............")
        print("WHO ARE YOU??????????")
        speakUp("Wait a minute.............")
        speakUp("WHO ARE YOU??????????")

        print(exception)
        return "None"
    print("query-->> ", query)
    return query


# search on wikipedia
def search_wikipedia(query):
    searchResults = wikipedia.search(query)  # collecting the search in an array
    if not searchResults:
        print('Sorry, Nothing found related to your query.')
        speakUp("Sorry, Nothing found related to our query.")
        return
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage.page(error.options[0])  # if error ocurrs we take the first error
    print(wikiPage.title)
    # collecting the search result summary
    wikiSummary = str(wikiPage.summary)
    return wikiSummary


def listOrDictionary(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']


def search_wolframalpha(query):
    # get the response from WolframAlpha of the query
    response = wolframClient.query(query)

    # @success: Wolfram Aplha was able to resolve the query
    # @numpods: Number of results returned
    # pod     : List of results. this can also contain subpods
    if response['@success'] == 'false':
        return "Could not compute"

    # Query resolved
    else:
        result = ''
        # Question
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]

        # May contain the answer, has the highest confidence value
        # If it's primary, or has the title of result or defination, then it's the official result
        if ('result' in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or (
                'definition' in pod1['@title'].lower()):
            # Get the result
            result = listOrDictionary(pod1['subpod'])
            # remove the bracketed part from the result
            return result.split('(')[0]
        else:
            question = listOrDictionary(pod0['subpod'])
            # remove the bracketed part from the result
            return result.split('(')[0]

            # search in wikipedia
            speakUp('Computing failed. Searching on wikipedia..')
            return search_wikipedia(question)


# Main loop

if __name__ == "__main__":
    speakUp("Hello there... What can i do for you??")
    # turning on the system
    while True:
        # make a list of what i said
        query = takeCommand().lower().split()
        print("QUERY:  ", query)

        # Checking for the Wakeup word first
        if query[0] == activationWord:
            query.pop(0)
            print("QUERY:  ", query)

            print(f'query---> {query}')
            # listing Commands
            if query[0] == "say":
                if "hello" in query:
                    print("hey")
                    speakUp("hye")
                else:
                    query.pop(0)  # removing the "say"
                    speech = " ".join(query)
                    speakUp((speech))

            # navigating to websites
            if query[0] == "go" and query[1] == "to":
                speakUp("opening...")
                query = " ".join(query[2:])
                webbrowser.get("chrome").open_new(query)

            # searching on wikipedia
            if query[0] == "wikipedia":
                query = " ".join(query[1:])
                speakUp("Searching on Wikipedia....")
                # collecting the search result
                result = search_wikipedia(query)
                speakUp(result)

            # Wolfram Alpha
            if query[0] == 'compute' or query[0] == "computer":
                query = " ".join(query[1:])
                speakUp("Computing..")
                try:
                    # searching the query in wolframaplha
                    result = search_wolframalpha(query)
                    print("result: ", result)
                    speakUp(result)
                except:
                    speakUp("Unable to compute.")

            # Taking note
            if query[0] == "log":
                speakUp("Ready to take note.")
                newNote = takeCommand().lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                # creating a file to take note
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(newNote)
                speakUp('Noted..')

            # Exit
            if query[0] == "exit":
                speakUp('Goodbye.')
                break
