package main

import (
	"database/sql"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

var db *sql.DB

func init() {
	// Database connection string
	connStr := os.Getenv("DB_URI")
	var err error

	// Open a connection to the database
	for {
		db, err = sql.Open("postgres", connStr)
		if err != nil {
			// panic(err)
			fmt.Println(err)
			time.Sleep(1 * time.Second)
			continue
		}
		break
	}

	// Test the connection
	for{
		err = db.Ping()
		if err != nil {
			// panic(err)
			fmt.Println(err)
			time.Sleep(1 * time.Second)
			continue
		}
		break
	}
	fmt.Println("Successfully connected to the database")
}

func main() {
	r := gin.Default()
	r.Use(cors.Default())

	// Health Check route
	r.GET("/healthz", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "Every thing is fine!"})
	})

	// Paginated blog articles route
	r.GET("/api/blog-articles", getBlogArticles)

	r.Run(":8080")
}

func getBlogArticles(c *gin.Context) {
	var rows *sql.Rows

	// Get limit from query parameters
	limit, err := strconv.Atoi(c.Query("limit"))
	if err != nil {
		limit = 10
	}

	// Get cursor from query parameters
	cursor := c.Query("cursor")

	// Query database based on cursor value
	if cursor == "" {
		query := "SELECT * FROM blog_articles ORDER BY id DESC limit $1;"
		rows, err = db.Query(query, limit)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal Server Error"})
			return
		}
	} else {
		query := "SELECT * FROM blog_articles WHERE id < $1 ORDER BY id DESC limit $2;"
		rows, err = db.Query(query, cursor, limit)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal Server Error"})
			return
		}
	}

	defer rows.Close()

	// Iterate through the result set and build a slice of articles
	articles := []gin.H{}
	for rows.Next() {
		var id, blogName, title, url string
		var description, image sql.NullString
		var date string

		err := rows.Scan(&id, &blogName, &url, &title, &description, &image, &date)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal Server Error"})
			return
		}

		article := gin.H{
			"id":          id,
			"blog_name":   blogName,
			"title":       title,
			"url":         url,
			"description": description,
			"image":       image,
			"date":        date,
		}
		articles = append(articles, article)
	}

	// Return the paginated list of blog articles
	c.JSON(http.StatusOK, gin.H{"articles": articles})
}
