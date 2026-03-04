# Day5 - SQL Validation Cases (API vs DB)

> Goal: Use SQL to validate API results (simulated DB seeded from API).
> DB: `reports/demo.db`

## Setup

```bash
python tools/seed_sqlite_from_api.py
```

Case 1 - Total count matches (posts)

Purpose: Validate total posts count (API vs DB)

SELECT COUNT(*) AS posts_cnt FROM posts;
Case 2 - Row exists by id (posts)

Purpose: Validate /posts/1 exists in DB

SELECT id, userId, title, body
FROM posts
WHERE id = 1;
Case 3 - Basic JOIN (posts -> users)

Purpose: Validate post has a valid user (foreign key)

SELECT p.id AS post_id, u.username
FROM posts p
JOIN users u ON u.id = p.userId
WHERE p.id = 1;
Case 4 - Orphan detection (LEFT JOIN)

Purpose: Find posts with missing user (should be 0)

SELECT COUNT(*) AS orphan_posts
FROM posts p
LEFT JOIN users u ON u.id = p.userId
WHERE u.id IS NULL;
Case 5 - GROUP BY count per user

Purpose: Count posts per user

SELECT userId, COUNT(*) AS post_cnt
FROM posts
GROUP BY userId
ORDER BY post_cnt DESC;
Case 6 - HAVING filter groups

Purpose: Users with >= 10 posts (HAVING is for grouped results)

SELECT userId, COUNT(*) AS post_cnt
FROM posts
GROUP BY userId
HAVING COUNT(*) >= 10
ORDER BY post_cnt DESC;
Case 7 - Comments count per post

Purpose: Validate comments distribution

SELECT postId, COUNT(*) AS comment_cnt
FROM comments
GROUP BY postId
ORDER BY comment_cnt DESC
LIMIT 10;
Case 8 - Validate a query param case (comments?postId=1)

Purpose: API query param should match DB filter

SELECT COUNT(*) AS comments_for_post_1
FROM comments
WHERE postId = 1;
Case 9 - Text quality check (empty titles)

Purpose: Title should not be empty (should be 0)

SELECT COUNT(*) AS empty_title_cnt
FROM posts
WHERE TRIM(title) = '';
Case 10 - Aggregate + WHERE vs HAVING

Purpose: Demonstrate WHERE filters rows; HAVING filters groups

WHERE example: only consider posts with id <= 50 before grouping

SELECT userId, COUNT(*) AS post_cnt
FROM posts
WHERE id <= 50
GROUP BY userId
ORDER BY post_cnt DESC;

HAVING example: filter groups after grouping

SELECT userId, COUNT(*) AS post_cnt
FROM posts
GROUP BY userId
HAVING COUNT(*) >= 5
ORDER BY post_cnt DESC;