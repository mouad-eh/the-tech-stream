import React, { useState, useEffect } from 'react';
import Header from "./components/header";
import CardGrid from "./components/cardGrid";

const fetchData = async () => {
  // Fetch initial data from your API or database
  const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/api/blog-articles?limit=10`);
  const data= await response.json();

  return data.articles;
};

export default async function Home() {
  const initialData = await fetchData()
  return (
    <div className="h-screen">
      <Header title="The Tech Stream"/>
      <CardGrid initialData={initialData}/>
    </div>
  );
}
