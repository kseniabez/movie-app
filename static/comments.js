document.addEventListener('DOMContentLoaded', function () {
    const pathParts = window.location.pathname.split('/').filter(Boolean);
    const isReviewPage = pathParts.length === 2 && pathParts[0] === 'review';

    if (isReviewPage) {
        const reviewId = pathParts[1];

        function fetchComments() {
            fetch('/api/v1/movies/comments/') // Fetch all comments
                .then(response => response.json())
                .then(data => {
                    const commentsContainer = document.getElementById('comments-container');
                    commentsContainer.innerHTML = '';

                    const filteredComments = data.filter(comment => comment.review == reviewId);

                    if (filteredComments.length === 0) {
                        commentsContainer.innerHTML = '<p>No comments yet.</p>';
                    } else {
                        filteredComments.forEach(comment => {
                            const commentElement = document.createElement('div');
                            commentElement.classList.add('comment-card');
                            commentElement.innerHTML = `
                                <div class="grid">
                                    <div>
                                        <a class="username" href="/user/${comment.user}">${comment.username}</a>
                                        <p><small>${new Date(comment.created_at).toLocaleString()}</small></p>
                                    </div>
                                    <p>${comment.content}</p>
                                </div>
                            `;
                            commentsContainer.appendChild(commentElement);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error fetching comments:', error);
                });
        }
        fetchComments()


        const form = document.getElementById('comment-form');
        if (form) {
            form.addEventListener('submit', function (event) {
                event.preventDefault();

                const formData = new FormData(form);
                let values = {};
                formData.append('review', reviewId);
                const csrfToken = formData.get('csrfmiddlewaretoken')?.toString();
                if (!csrfToken) {
                    console.error('CSRF token is missing or invalid.');
                    return;
                }
                for (let [key, value] of formData.entries()) {
                    console.log(`${key}: ${value}`);
                    values[key] = value;
                }

                fetch('/api/v1/movies/comments/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(values),
                })
                    .then(response => {
                        if (response.ok) {
                            return response.json();
                        }
                        throw new Error('Error posting comment');
                    })
                    .then(data => {
                        if (data.id) {
                            fetchComments();
                            form.reset();
                        }
                    })
                    .catch(error => {
                        console.error('Error posting comment:', error);
                    });
            });
        }
    }
});
