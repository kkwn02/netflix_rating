//Event listener for message sent when tab is updated
chrome.runtime.onMessage.addListener((obj, sender, response) => {
    // Make sure DOM is loaded 
    if (document.readyState !== 'loading') {
        displayContents();
    } else {
        document.addEventListener('DOMContentLoaded', () => {
            displayContents();
        });
    }
    response({"res": "SUCCESS"});
});

// Return an array of objects containing title and id
displayContents = async () => {
    let sliders = document.getElementsByClassName("lolomoRow lolomoRow_title_card css-0");
    //Private server   
    const url = 'secret';
    for (let slider of sliders) {
        let collection = slider.querySelectorAll("a[href^='/watch']");
        const promises = [];
        const contentDict = {};
        for (let title of collection) {
            const content = {};
            const regex = /([0-9]+)/;
            thumbnailContainer = title.children[0];
            content["title"] = title.getAttribute("aria-label");
            content["id"] = title.getAttribute("href").match(regex)[0];
            let data = JSON.stringify(content);
            promises.push(fetch(url, {
                method: 'POST',
                mode: 'cors',
                body: data
            }));
            contentDict[content["title"]] = thumbnailContainer;
        }
        Promise.all(promises).then(responses => {
            responses.forEach(response => {
                addLabel(contentDict, response.json());
            })
        }).catch(err => {
            console.log("ERROR: couldn't fetch ratings")
        });
        break;
    }    
}

const addLabel = async (contentDict, response) => {
    let jsonRes = await response;
    console.log(jsonRes);
    thumbnailContainer = contentDict[jsonRes["title"]];
    const thumbnail = thumbnailContainer.children[0];
    const ratingLabel = createLabel(jsonRes["rating"], thumbnail);
    const triangle = createTriangle(thumbnail);
    thumbnailContainer.appendChild(ratingLabel);
    thumbnailContainer.appendChild(triangle);
}
//Create rating label 
const createLabel = (rating, thumbnail) => {
    const element = document.createElement("div");
    element.classList.add("overlay_image");
    element.innerHTML = rating;
    element.style.right = (thumbnail.offsetWidth*0.02)+"px";
    element.style.width = (thumbnail.offsetWidth*0.15)+"px";
    element.style.height = (thumbnail.offsetHeight*0.3)+"px";
    element.style.lineHeight = (thumbnail.offsetHeight*0.3)+"px";
    element.style.fontSize = (thumbnail.offsetWidth*0.08)+"px";
    return element;
}

//Create triangle
const createTriangle = (thumbnail) => {
    const element = document.createElement("div");
    element.classList.add("triangle");
    element.style.right = (thumbnail.offsetWidth*0.02)+"px";
    element.style.top = (thumbnail.offsetHeight*0.3)+"px";
    element.style.borderRightWidth = (thumbnail.offsetWidth*0.075)+"px";
    element.style.borderLeftWidth = (thumbnail.offsetWidth*0.075)+"px";
    element.style.borderBottomWidth = (thumbnail.offsetHeight*0.2)+"px";
    return element;
}