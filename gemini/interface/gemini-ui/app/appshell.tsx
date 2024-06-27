"use client";

import { AppShell, Group, Burger, Stack, Skeleton, Text, Box, Divider } from '@mantine/core';
import { AppShellNavbar, AppShellHeader, AppShellMain } from '@mantine/core';
import { NavLink } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import Logo from './logo';


// Icons
import {
  IconHome,
  IconUpload,
  IconDrone,
  IconPlant
} from '@tabler/icons-react';

const navbarLinks = [
    { title: 'Home', href: '/' , icon: IconHome},
    { title: 'Upload', href: '/upload', icon: IconUpload },
    { title: 'Sensors', href: '/sensors', icon: IconDrone },
    { title: 'Traits', href: '/traits', icon: IconPlant }
];


export default function GEMINIAppShell() {
    
    const [mobileOpened, { toggle: toggleMobile }] = useDisclosure();
    const [desktopOpened, { toggle: toggleDesktop }] = useDisclosure(true);
  

    const links = navbarLinks.map((link) => (
      <>
        <Group key={link.title} gap="lg">
          {link.icon && <link.icon size={22} />}
          <Text size="lg" fw={600}> {link.title} </Text>
        </Group>
        <Divider />
      </>
    ));

    return (
      <AppShell
        header={{ height: 60 }}
        navbar={{
          width: 300,
          breakpoint: 'sm',
          collapsed: { mobile: !mobileOpened, desktop: !desktopOpened },
        }}
        padding="md"
      >
        <AppShellHeader>
          <Group h="100%" px="md">
            <Burger opened={mobileOpened} onClick={toggleMobile} hiddenFrom="sm" size="sm" />
            <Burger opened={desktopOpened} onClick={toggleDesktop} visibleFrom="sm" size="sm" />
            <Logo />
          </Group>
        </AppShellHeader>
        <AppShellNavbar p="md">
            <Stack gap="md">{links}</Stack>
        </AppShellNavbar>
        <AppShellMain bg={"white"}></AppShellMain>
      </AppShell>
    );
  }