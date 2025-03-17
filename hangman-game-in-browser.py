import random  # For selecting random words
import streamlit as st  # Streamlit for GUI

def get_word(difficulty):
    """Returns a random word based on the selected difficulty."""
    words = {
        'easy': ['apple', 'ball', 'cat', 'dog', 'fish'],
        'medium': ['python', 'rocket', 'jungle', 'laptop', 'mobile'],
        'hard': ['elephant', 'avalanche', 'dictionary', 'university', 'javascript']
    }
    return random.choice(words[difficulty])

def display_hangman(attempts):
    """Returns the hangman stage based on remaining attempts."""
    stages = ["🪂", "😵", "😨", "😰", "😥", "😧", "😀"]  # Hangman stages from losing to full health
    return stages[attempts]

def main():
    st.title("Hangman Game")
    
    # Initialize session state variables if not already present
    if 'word' not in st.session_state:
        st.session_state.word = ""
        st.session_state.word_letters = set()
        st.session_state.guessed_letters = set()
        st.session_state.attempts = 6  # Total attempts allowed
        st.session_state.difficulty = ""
    
    if st.session_state.word == "":
        # Difficulty selection
        st.subheader("Choose Difficulty")
        difficulty = st.radio("Select difficulty:", ('easy', 'medium', 'hard'))
        if st.button("Start Game"):
            st.session_state.word = get_word(difficulty)
            st.session_state.word_letters = set(st.session_state.word)
            st.session_state.difficulty = difficulty
            st.rerun()  # Restart UI to reflect changes
    else:
        # Game in progress
        st.subheader("Guess the Word")
        st.write(display_hangman(st.session_state.attempts))  # Show current hangman state
        
        # Display the word with guessed letters revealed
        st.write("Word:", " ".join([letter if letter in st.session_state.guessed_letters else '_' for letter in st.session_state.word]))
        
        # Alphabet buttons for guessing letters
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        cols = st.columns(9)  # Creating columns for button layout
        for index, letter in enumerate(alphabet):
            with cols[index % 9]:
                if st.button(letter):
                    if letter in st.session_state.guessed_letters:
                        st.warning("You already guessed that letter!")
                    elif letter in st.session_state.word_letters:
                        st.session_state.word_letters.remove(letter)
                        st.session_state.guessed_letters.add(letter)
                    else:
                        st.session_state.attempts -= 1  # Reduce attempts if wrong guess
                        st.session_state.guessed_letters.add(letter)
                    st.rerun()  # Update UI state
        
        # Winning condition
        if not st.session_state.word_letters:
            st.success(f"Congratulations! You guessed the word: {st.session_state.word}")
            if st.button("Play Again"):
                st.session_state.word = ""
                st.rerun()
        # Losing condition
        elif st.session_state.attempts == 0:
            st.error(f"Game Over! The word was: {st.session_state.word}")
            if st.button("Try Again"):
                st.session_state.word = ""
                st.rerun()

# Run the game
if __name__ == "__main__":
    main()
