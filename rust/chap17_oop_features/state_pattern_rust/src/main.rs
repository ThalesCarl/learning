use state_pattern::Post;

fn main() {
    let mut post = Post::new(); // Creates a DraftPost struct instead

    post.add_text("I ate a salad for lunch today");

    let post.request_review(); // Shadow create a PendingReviewPost

    let post.approve(); // Shadow create a Post
    assert_eq!("I ate a salad for lunch today", post.content());
}
