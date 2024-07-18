import { AppShell } from "@mantine/core";
import { Burger, Group, Text } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import Logo from "@/components/logo/logo";
import classes from './shell.module.css';
import { Link } from "react-router-dom";
import ExperimentSelector from "@/components/experimentselector/experimentselector";

// Icons
import {
    IconHome,
    IconUpload,
    IconDrone,
    IconPlant
  } from '@tabler/icons-react';
  
const navbarLinks = [
    { title: 'Home', href: '/' , icon: IconHome},
    { title: 'Upload Data', href: '/upload', icon: IconUpload },
    { title: 'Sensors', href: '/sensors', icon: IconDrone },
    { title: 'Traits', href: '/traits', icon: IconPlant },
];


export default function Shell({children} : Readonly<{children: React.ReactNode}>) {
    const [mobileOpened, { toggle: toggleMobile }] = useDisclosure();
    const [desktopOpened, { toggle: toggleDesktop }] = useDisclosure(true);

    const links = navbarLinks.map((link) => (
        <Link to={link.href} key={link.title} className={classes.link}>
            <Group p="sm">
            {link.icon && <link.icon size={22} />}
            <Text size="lg" fw={600}>
                {link.title}
            </Text>
            </Group>
        </Link>
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
        <AppShell.Header>
          <Group justify='space-between' align='center' h='100%'>
            <Group h="100%" px="md">
              <Burger opened={mobileOpened} onClick={toggleMobile} hiddenFrom="sm" size="sm" />
              <Burger opened={desktopOpened} onClick={toggleDesktop} visibleFrom="sm" size="sm" />
              <Logo />
            </Group>
            <Group h="100%" px="md">
              <ExperimentSelector />
            </Group>
          </Group>
          <AppShell.Navbar>{links}</AppShell.Navbar>
        </AppShell.Header>
        <AppShell.Main>
          {children}
        </AppShell.Main>
      </AppShell>
    );
}