import { Navbar } from "flowbite-react";

export function PwCNavbar() {
  return (
    <Navbar fluid rounded className="fixed top-0 left-0 w-full bg-white dark:bg-gray-900 shadow-lg z-10">
      <Navbar.Brand>
        <img src="/PwC-logo.svg" className="mr-3 h-6 sm:h-9" alt="Company Logo" />
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
          Gen AI Legal Assistant
        </span>
      </Navbar.Brand>
    </Navbar>
  );
}
