# Things I've learned from this project

## Bootstrapping phase
- You can't ADD files to a Docker image from outside the current context. (I think this means you can only `ADD` files from the same directory that holds your `Dockerfile`.)
- ~~Working with tarfiles is a pain in the neck.~~
- ~~Working wiht tempfiles is a pain in the neck.~~ 
- Working with file paths is hard. Read the docs! Do methods want a relative path? Absolute path?
- [Miguel Grinberg](https://blog.miguelgrinberg.com/post/about-me) has written an [awesome (mega) Flask tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). Thank you!
- Pass `--rm` to `docker run`. This automatically removes the container when it closes.
- Understand user space. Docker builds as root, is it run as root? Who can view files? I posted a [StackOverflow question](https://stackoverflow.com/questions/60595037/using-flask-send-from-directory-from-a-docker-container-returns-an-empty-tar-gz)