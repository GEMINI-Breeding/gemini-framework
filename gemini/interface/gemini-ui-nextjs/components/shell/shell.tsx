"use client";

import { AppShell, Group, Burger, Stack, Text} from '@mantine/core';
import { AppShellNavbar, AppShellHeader, AppShellMain } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import Logo from '@/app/logo';
import classes from './shell.module.css';
import Link from "next/link";

// Icons
import {
  IconHome,
  IconUpload,
  IconDrone,
  IconPlant,
  IconFlask2,
  IconMap
} from '@tabler/icons-react';
import ExperimentSelector from '../experimentselector/experimentselector';

const navbarLinks = [
    { title: 'Home', href: '/' , icon: IconHome},
    { title: 'Upload Data', href: '/upload', icon: IconUpload },
    { title: 'Experiments', href: '/experiments', icon: IconFlask2 },
    { title: 'Sensors', href: '/sensors', icon: IconDrone },
    { title: 'Traits', href: '/traits', icon: IconPlant },
    { title: 'Locations', href: '/locations', icon: IconMap }
];


export default function Shell({children} : Readonly<{children: React.ReactNode}>) {
    
    const [mobileOpened, { toggle: toggleMobile }] = useDisclosure();
    const [desktopOpened, { toggle: toggleDesktop }] = useDisclosure(true);

    const links = navbarLinks.map((link) => (
        <div key={link.title} className={classes.link}>
            <Group>
            {link.icon && <link.icon size={22} />}
            <Text size="lg" fw={600}>
                <Link href={link.href} passHref>
                    {link.title}
                </Link>
            </Text>
            </Group>
        </div>
    ));

    return (
      <AppShell
        header={{ height: 60 }}
        navbar={{
          width: 225,
          breakpoint: 'sm',
          collapsed: { mobile: !mobileOpened, desktop: !desktopOpened },
        }}
        padding="md"
        className={classes.main}
      >
        <AppShellHeader>
          <Group justify='space-between' align='center' h='100%'>
            <Group h="100%" px="md">
              <Burger opened={mobileOpened} onClick={toggleMobile} hiddenFrom="sm" size="sm" />
              <Burger opened={desktopOpened} onClick={toggleDesktop} visibleFrom="sm" size="sm" />
              <Logo />
            </Group>
            <Group h="100%" px="md">
            </Group>
          </Group>
        </AppShellHeader>
        <AppShellNavbar p="md">
            <Stack gap="xs">{links}</Stack>
        </AppShellNavbar>
        <AppShellMain className={classes.main}>{children}</AppShellMain>
      </AppShell>
    );
  }