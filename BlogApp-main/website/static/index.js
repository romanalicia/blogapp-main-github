
function like(postsId) {

    const likeCount = document.getElementById(`likes-count-${postsId}`);
    const likeButton = document.getElementById(`like-button-${postsId}`);
    fetch(`/like-posts/${postsId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        likeCount.innerHTML = data["likes"];
        if (data["liked"] === true) {
          likeButton.className = "fas fa-thumbs-up";
        } else {
          likeButton.className = "far fa-thumbs-up";
        }
      })
      .catch((e) => alert("Could not like post."));
  }
  
   