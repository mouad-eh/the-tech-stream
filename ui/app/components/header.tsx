interface HeaderProps {
    title: string;
  }
  
export default function Header({ title }: HeaderProps) {
  return (
    // <header className="bg-gray-50 text-black p-4 border-b-2 border-black flex justify-between items-center">
    <header className="bg-gray-50 text-black p-4 border-b-2 border-black flex justify-center items-center">
      <h1 className="text-xl font-bold">{title}</h1>
      {/* <nav>
        <ul className="flex text-sm space-x-4">
          <li><a href="#">Sign up</a></li>
          <li><a href="#">Sign in</a></li>
        </ul>  
      </nav> */}
    </header>
  );
}