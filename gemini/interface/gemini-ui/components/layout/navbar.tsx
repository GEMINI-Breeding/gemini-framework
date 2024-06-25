"use client";

import {Navbar as NextUINavbar, NavbarBrand, NavbarContent, NavbarItem, NavbarMenuToggle, NavbarMenu, NavbarMenuItem} from "@nextui-org/navbar"
import {Button} from "@nextui-org/button"
import {Link} from "@nextui-org/link"
import NavbarLogo from "./navbar-logo"
import {useState} from "react"

const menuItems = {
    "Home": "/",
    "Experiments": "/experiments",
    "Sensors": "/sensors",
    "Traits": "/traits",
    "Plots": "/plots",
    "Processes": "/processes",
    "Models": "/models"
}

export default function LayoutNavbar() {
    const [isMenuOpen, setIsMenuOpen] = useState(false)

    return (
        <NextUINavbar onMenuOpenChange={setIsMenuOpen}>
        <NavbarContent>
            <NavbarMenuToggle
            aria-label={isMenuOpen ? "Close menu" : "Open menu"}
            className="sm:hidden"
            />
            <NavbarBrand>
            <NavbarLogo />  
            </NavbarBrand>
        </NavbarContent>
        <NavbarContent className="hidden sm:flex gap-4" justify="center">
            <NavbarItem>
            <Link color="foreground" href="#">
                Home
            </Link>
            </NavbarItem>
            <NavbarItem isActive>
            <Link href="#" aria-current="page">
                About Us
            </Link>
            </NavbarItem>
            <NavbarItem>
            <Link color="foreground" href="#">
                Contact
            </Link>
            </NavbarItem>
        </NavbarContent>
        <NavbarMenu>
            {Object.entries(menuItems).map(([label, href]) => (
            <NavbarMenuItem key={label}>
                <Link href={href}>{
                    label
                }</Link>
            </NavbarMenuItem>
            ))}
        </NavbarMenu>
        </NextUINavbar>
    );
}
