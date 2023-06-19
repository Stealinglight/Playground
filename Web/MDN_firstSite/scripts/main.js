    // main.js


const myHeading = document.querySelector('h1');
myHeading.textContent = 'Sansa Cat';

document.querySelector('html').addEventListener('click', () => {
    alert('Ouch! Stop poking me!');
});


const myImage = document.querySelector('img');

myImage.onclick = () => {
    const mySrc = myImage.getAttribute('src');
    if (mySrc === 'images/IMG_7285.jpg') {
        myImage.setAttribute('src', 'images/IMG_5649.jpg');
    } else {
        myImage.setAttribute('src', 'images/IMG_7285.jpg');
    }
};

let myButton = document.querySelector('button');
let myHeading = document.querySelector('h1');

function setUserName() {
    const myName = prompt('Please enter your name.');
    localStorage.setItem('name', myName);
    myHeading.textContent = 'Sansa Cat is cool, ${myName}';
}

if (!localStorage.getItem('name')) {
    setUserName();
} else {
    const storedName = localStorage.getItem('name');
    myHeading.textContent = 'Sansa Cat is cool, ${storedName}';
}

myButton.onclick = () => {
    setUserName();
};

function setUserName() {
    let myName = prompt('Please enter your name.');
    if (!myName) {
        setUserName();
    } else {
        localStorage.setItem('name', myName);
        myHeading.innerHTML = 'Sansa Cat is cool, ${myName}';
    }
}