const allPosts = document.querySelector("#all-posts")
const following = document.querySelector("#following")
const profile = document.querySelector("#profile")
following.style.display = "none"
profile.style.display = "none"
const ids = ["display-posts", "follow-posts", "profile-posts"]
let page = 1
paginatedPostCreation(`/allPost/${page}`, "#morePost", "#display-posts")

document.querySelector("#morePost").addEventListener("click", () => {paginatedPostCreation(`/allPost/${page}`, "#morePost", "#display-posts")})

document.querySelector("#link-allPosts").addEventListener("click", () => {
    // Show all posts and hide the others
    following.style.display = "none"
    allPosts.style.display = "block"
    profile.style.display = "none"

    page = 1

    /*document.querySelector("#compose-form").addEventListener('submit', () =>{
        content = document.querySelector("#content").value
        console.log("HAS")
        fetch("compose", {
            method: "POST",
            body: JSON.stringify({
                content: content
            })
        })
        .then(response => response.json())
        .then(posted => console.log(posted))
    } ) */
    // Get the posts
    paginatedPostCreation(`/allPost/${page}`, "#morePost", "#display-posts")
})

document.querySelector("#link-following").addEventListener("click", () => {
    // Show following and hide the others
    following.style.display = "block"
    allPosts.style.display = "none"
    profile.style.display = "none"

    // Get the usernames of followed users
    fetch("/followings")
    .then(response => response.json())
    .then(followings => {
        // get the container element
        follow = document.querySelector("#follow")
        // delete previously created divs
        while (follow.firstChild) {
            follow.removeChild(follow.lastChild);
        }
        // if no posts, show a message
        if(followings.length == 0){
            li = document.createElement("li")
            li.innerText = "Currently you don't follow anyone"

            follow.append(li)
        }
        // create lis for follows
        else{
            followings.forEach(followed => {
                li = document.createElement("li")
                li.innerText = followed.followed

                follow.append(li)
            })
        }
    })

    // Get all the posts of followed users
    fetch("/followingPosts")
    .then(response => response.json())
    // Create div for the posts
    .then(posts => { 
        postCreationPreparation(posts, "#follow-posts", "Currently they have no posts") 
    })
})


function loadProfilePage(username){
    // Show profile page and hide the others
    following.style.display = "none"
    allPosts.style.display = "none"
    profile.style.display = "block"

    page = 1

    document.querySelector("#morePostProfile").addEventListener("click", () => {paginatedPostCreation(`/profilePagePosts/${username}/${page}`, "#morePostProfile", "#profile-posts")})
    
    // Get the selected user's datas
    fetch(`/profilePage/${username}`)
    .then(response => response.json())
    .then(datas => {
        document.querySelector("#username").innerHTML = datas.username
        document.querySelector("#followers").innerHTML = `Number of followers: ${datas.followers}`
        document.querySelector("#followed").innerHTML = `Follow: ${datas.followed}`

        fetch("getCurrentUser")
        .then(response =>response.json())
        .then(loggedInUser => {
            button = document.querySelector("#followOrUnfollow")
            if(loggedInUser.username == username){
                button.style.display = "none"
            }
            else{
                button.style.display = "block"
                fetch(`followOrUnfollow/${username}`)
                .then(response => response.json())
                .then(follow => {
                    if(follow.followed) button.innerText = "Unfollow"
                    else button.innerText = "Follow"
                    button.addEventListener("click", (event) => { 
                        event.stopImmediatePropagation();
                        doFollowOrUnfollow(username, datas) 
                    })
                })
            }
        })
    })
    // Get the selected users posts
    paginatedPostCreation(`/profilePagePosts/${username}/${page}`, "#morePostProfile", "#profile-posts")
    //"This user haven't posted yet :("
}

function doFollowOrUnfollow(selectedUsername, datas){
    fetch(`doFollowOrUnfollow/${selectedUsername}`)
        .then(response => response.json())
        .then(success => {
            console.log(success)
            if(success.save == "Followed") {
                button.innerText = "Unfollow"
                datas.followers += 1
            }
            else {
                button.innerText = "Follow"
                datas.followers -= 1
            }
            document.querySelector("#followers").innerHTML = `Number of followers: ${datas.followers}`
        })
}

function postCreationPreparation(posts, id, nothing){
    // get the container element
    post = document.querySelector(id)
    // delete previously created posts
    if (page == 1){
        ids.forEach(selectedId => {
            container = document.querySelector(`#${selectedId}`)
            while (container.firstChild) {
                container.removeChild(container.lastChild);
            }
        })
    }
    
    // if no posts, show a message
    if(posts.length == 0){
        div = document.createElement("div")
        div.innerText = nothing

        post.append(div)
    }
    else{
        //Foreach nem nagyon kompatibilis az async dolgokkal, helyette promise.all + map
        /*posts.forEach(profilePost => {
            fetch(`alreadyLiked/${profilePost.id}`)
                .then(response => response.json())
                .then(liked => {
                    postCreation(profilePost, liked.liked)
                    post.append(div)
                })
        })*/

        // create divs for posts now for real
        const fetchPromises = posts.map(profilePost => {
            return fetch(`alreadyLiked/${profilePost.id}`)
              .then(response => response.json())
        });
          
        Promise.all(fetchPromises)
        .then(results => {
            results.forEach((liked, index) => {
            const profilePost = posts[index];
            postCreation(profilePost, liked.liked);
            post.append(div);
            });
        });                                      
    }
}

function postCreation(post, liked) {   
    // Create HTML elements for the data
    div = document.createElement("div")
    div.classList.add("post")
    user = document.createElement("p")
    content = document.createElement("p")
    date = document.createElement("p")
    likes = document.createElement("div")
    likes.setAttribute("id", `like${post.id}`)
    // Fill the elements with data
    user.innerHTML = `<a href="#">${post.user}</a>`
    user.classList.add("inline")
    content.innerText = post.content
    date.innerText = post.date
    if(!liked) {
        likes.innerHTML = `<img src="static/network/like.png" alt="" id="likeImg${post.id}"> <span id="likeCounter${post.id}">${post.likes}</span>`
    }
    else{
        likes.innerHTML = `<img src="static/network/liked.png" alt="" id="likeImg${post.id}"> <span id="likeCounter${post.id}">${post.likes}</span>`
    }
    // Add eventlistener for liking the post
    likes.addEventListener("click", function(event){ 
        event.stopImmediatePropagation();
        liking(post, liked) 
    })
    likes.classList.add("inline")
    // Add eventlistener for loading profile page
    user.addEventListener("click", function(){loadProfilePage(post.user)})
    // add elements to the container
    div.append(user, content, date, likes)
}

function liking(post){
    console.log(post)
    fetch(`doLikeOrUnlike/${post.id}`)
        .then(response => response.json())
        .then(data => {
            likes = document.querySelector(`#like${post.id}`)
            numberOfLikes = parseInt(document.querySelector(`#likeCounter${post.id}`).innerText)
            if(data.liked){
                likes.innerHTML = `<img src="static/network/liked.png" alt="" id="likeImg${post.id}"> <span id="likeCounter${post.id}">${numberOfLikes+1}</span>`
            }
            else{
                likes.innerHTML = `<img src="static/network/like.png" alt="" id="likeImg${post.id}"> <span id="likeCounter${post.id}">${numberOfLikes-1}</span>`
            }
        })
}

function paginatedPostCreation(fetcher, buttonId, displayDivID){
    console.log(fetcher)
    fetch(fetcher)
    .then(response => response.json())
    // Create div for all posts
    .then(posts => { 
        postCreationPreparation(posts[0], displayDivID, "There are absolutely no posts :(") 
        page++
        if(posts[1]){
            document.querySelector(buttonId).style.display = "block"
        }
        else{
            document.querySelector(buttonId).style.display = "none"
        }
    })
}