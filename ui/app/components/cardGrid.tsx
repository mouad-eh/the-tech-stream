"use client";

import React, { useState, useEffect } from 'react';
import Card from './card';
import { useInView } from 'react-intersection-observer'

interface Post {
    id: string;
    blog_name: string;
    title: string;
    url: string;
    description: {
        String: string;
        Valid: boolean;
    };
    image: {
        String: string;
        Valid: boolean;
    };
    date: string;
}

interface CardGridProps {
  initialData: Post[]
}


export default function CardGrid({initialData}: CardGridProps) {
    const { ref, inView } = useInView();
    const [data, setData] = useState<Post[]>(initialData);
    const [allLoaded, setAllLoaded] = useState<boolean>(false);

    const fetchMoreData = async () => {
      // Fetch more data when scrolling
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/api/blog-articles?limit=10&cursor=${data[data.length - 1].id}`);
      const moreData = await response.json();
      const morePosts = moreData.articles

      if(morePosts.length == 0){
        setAllLoaded(true);
      }
      // Update the state with the new data
      setData((prevData: Post[]) => [...prevData, ...morePosts]);
    };

    useEffect(() => {
      if (inView){
        fetchMoreData()
      }
    }, [inView]);

    return(
      <main className="p-4 bg-gray-50 text-black ">
        <section className='flex flex-row flex-wrap gap-5 justify-center'>
          {data.map(post => (
            <Card key={post.title} title={post.title} blog_name={post.blog_name}
            url={post.url} image={post.image.String}
            date={post.date} description={post.description.String}
            />
          ))}
        </section>
        <div ref={ref} className='pt-4 text-center'>
          {!allLoaded ? "Loading..." : null}
        </div>
      </main>
    );
}