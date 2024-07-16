import { AppShell, AppShellNavbar, AppShellHeader, AppShellMain } from "@mantine/core";
import { Group, Burger, Stack, Text} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from './shell.module.css';
import Logo from "../logo/logo";

// Icons for the navbar
import {
  IconHome,
  IconUpload,
  IconDrone,
  IconPlant,
  IconFlask2,
  IconMap
} from '@tabler/icons-react';

const navbarLinks = [
    { title: 'Home', href: '/' , icon: IconHome},
    { title: 'Upload', href: '/upload', icon: IconUpload },
    { title: 'Sensors', href: '/sensors', icon: IconDrone },
    { title: 'Traits', href: '/traits', icon: IconPlant },
];

export default function Shell({children} : Readonly<{children: React.ReactNode}>) {

    const [mobileOpened, { toggle: toggleMobile }] = useDisclosure();
    const [desktopOpened, { toggle: toggleDesktop }] = useDisclosure(true);

    const links = navbarLinks.map((link) => (
        <div key={link.title} className={classes.link}>
            <Group>
            {link.icon && <link.icon size={22} />}
            <Text size="lg" fw={600}>
                {link.title}
            </Text>
            </Group>
        </div>
    ));

    return (
      <AppShell
        header={{ height: 60 }}
        navbar={{ width: 225, breakpoint: 'sm', collapsed: { mobile: !mobileOpened, desktop: !desktopOpened } }}
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
