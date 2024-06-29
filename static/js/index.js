let num_to_display = get_num_to_display();
let start_card = 0;
let end_card = num_to_display - 1;

document.addEventListener("DOMContentLoaded", function() {
    let next_btn = document.querySelectorAll(".next-btn");
    let previous_btn = document.querySelectorAll('.previous-btn');

    let card_container = document.querySelector('.card-slider');
    let cards = card_container.querySelectorAll(".card");

    card_num = cards.length;
    console.log(cards);

    hide_all(start_card, end_card, cards);
    console.log(previous_btn)   
    
    next_btn.forEach(next => {
        next.addEventListener('click', function(){
            console.log(next )

            if (end_card < card_num - 1) { // Check if there are more cards to display
                show_next_cards(cards, start_card, end_card); 
            }
        });
    });
    previous_btn.forEach(previous => {
        previous.addEventListener('click', function(){
            if (start_card > 0) { // Check if there are previous cards to display
                show_previous_cards(cards, start_card, end_card); 
            }
        });
    });

    
    window.addEventListener('resize', function() {
        console.log("start :"+start_card + " end : "+end_card);
        console.log('num_to_display : ' +num_to_display);
    
        num_to_display = get_num_to_display();
        start_card = 0;
        end_card = num_to_display - 1;
        hide_all(start_card, end_card, cards);
    });

});


function hide_all(start, end, cards_array){
    for (let i = 0; i < cards_array.length; i++) {
        console.log("up");
        if(i>= start && i<=end){
            show(cards_array[i])
            continue;
        }
        hide(cards_array[i]);
        console.log("down");
    }
}

function hide(element) {
    element.style.display='none';
}

function show(element) {
    element.style.display='flex';
}

function show_next_cards(cards_array, start, end) {
    hide(cards_array[start]); // Hide the first card of the current set
    show(cards_array[end + 1]); // Show the next card
    // Update indices for the next set of cards
    start_card++;
    end_card++;

    console.log("start :"+start_card + " end : "+end_card);
}

function show_previous_cards(cards_array, start, end) {
    hide(cards_array[end]); // Hide the last card of the current set
    show(cards_array[start - 1]); // Show the previous card
    // Update indices for the previous set of cards
    start_card--;
    end_card--;
}
function get_num_to_display() {
    const screenWidth = window.innerWidth;
    let numToDisplay;

    if (screenWidth < 768) {
        // For phone size (screens less than 768px width)
        numToDisplay = 1;
    }else if (screenWidth >= 768 && screenWidth < 990) {
        // For tablet size (screens between 768px and 1024px width)
        numToDisplay = 2;
    }
     else if (screenWidth >= 990 && screenWidth < 1286) {
        // For tablet size (screens between 768px and 1024px width)
        numToDisplay = 3;
    } else {
        // For PC size (screens greater than or equal to 1024px width)
        numToDisplay = 4;
    }
    return numToDisplay;
}
function set_end() {
    end_card = get_num_to_display()-1
}
