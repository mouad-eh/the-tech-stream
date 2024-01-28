import Image from "next/image";

interface CardProps {
    blog_name: string;
    title: string;
    url: string;
    description: string;
    image: string;
    date: string;
  }
  
  export default function Card({ blog_name, title, url, description, image, date  }: CardProps) {
    const dateObj: Date = new Date(date)
    let year = dateObj.getFullYear();
    let month = dateObj.getMonth() + 1; 
    let day = dateObj.getDate();

    // Create a formatted date string
    let formattedDateString = `${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`;
    const handleClick = () => {
      window.open(url, '_blank');
    }
    return (
      <div onClick={handleClick} className="h-96 w-96 bg-white rounded-xl overflow-hidden shadow-lg flex flex-col">
        <img className="w-full h-48 object-cover" src={image} alt={title} />
        <div className="p-6 flex flex-col justify-between flex-1">
          <div className="font-bold text-xl">{title}</div>          
          <div className="flex justify-between items-end">
            <p className="text-gray-700 text-base">{blog_name}</p>
            <p className="text-gray-700 text-base">{formattedDateString}</p>
          </div>
        </div>
      </div>
    );
  }

