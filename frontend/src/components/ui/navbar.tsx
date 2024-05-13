// import Link from "next/link";
import { Navbar } from "flowbite-react";

export function PwCNavbar() {
  return (
    <Navbar fluid rounded>
      <Navbar.Brand >
        <img src="/PwC-logo.svg" className="mr-3 h-6 sm:h-9" alt="Flowbite React Logo" />
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Gen AI Legal Assistant</span>
      </Navbar.Brand>
      
    </Navbar>
  );
}