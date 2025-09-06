<script>
  import {
    A,
    P,
    Li,
    Button,
    Modal,
    Heading,
    Navbar,
    NavBrand,
    Tooltip,
    DarkMode,
  } from "flowbite-svelte";
  import {
    AdjustmentsHorizontalSolid,
    PlusOutline,
    QuestionCircleOutline,
    GithubSolid,
    ListOutline,
    ChartOutline,
  } from "flowbite-svelte-icons";
  import surveys from "./data/other-surveys.json";
  import AddEntry from "./components/addEntry.svelte";

  let open = false;
  let menu;
  export let detailView;
  export let topView;
  export let freq;
  export let closeFn;
  export let showTitle;
  export let headerPx;
  export let toggleParams;

  let pill = true;

</script>

<header style="max-height:{headerPx}px;">
  <Navbar class="mx-0" style="height:{headerPx}px">
    <div class="flex float-left {showTitle ? 'hidden' : ''}">
      <Button
        {pill}
        outline
        class="!p-1 border-0 mr-5"
        id="toggle-filters"
        on:click={closeFn}
      >
        <AdjustmentsHorizontalSolid />
        <Tooltip triggeredBy="#toggle-filters" placement="bottom">
          Toggle Filters
        </Tooltip>
      </Button>

      <NavBrand class="items-left">
        {#if topView.title}
          <Heading tag="h6">
            {topView.title}
          </Heading>
        {/if}
      </NavBrand>

      <Button
        {pill}
        outline
        class="!p-1 border-0  ml-5 {toggleParams.hidden ? 'hidden' : ''}"
        id="toggle-view"
        on:click={toggleParams.func}
      >
        {#if toggleParams.vis}
          <ListOutline />
        {/if}
        {#if toggleParams.papers}
          <ChartOutline />
        {/if}
        <Tooltip triggeredBy="#toggle-view" placement="bottom">
          Toggle View
        </Tooltip>
      </Button>
    </div>

    {#if showTitle}
      <div class="flex float-left items-center"></div>
    {/if}

    <div class="float-right hidden lg:flex">
      
      <Modal size="lg" title="Add entry" bind:open autoclose={false}>
        <AddEntry {detailView} {freq} addEntryInfo={topView.addEntry} />
      </Modal>
      
      <Button
        {pill}
        outline
        class="!p-1 border-0"
        id="add-entry"
        on:click={() => (open = true)}
      >
        <PlusOutline class="w-4 h-4" />
        <Tooltip triggeredBy="#add-entry" placement="bottom">Add entry</Tooltip>
      </Button>

      <Button
        {pill}
        outline
        class="!p-1 border-0"
        id="github-link"
        on:click={() => window.open(topView.addEntry.github, "_blank")}
      >
        <GithubSolid />
        <Tooltip triggeredBy="#github-link" placement="bottom">GitHub</Tooltip>
      </Button>

      <Button
        {pill}
        outline
        class="!p-1 border-0"
        id="other-surveys"
        on:click={() => (menu = true)}
      >
        <QuestionCircleOutline />
        <Tooltip triggeredBy="#other-surveys" placement="bottom">About</Tooltip>
      </Button>

      <Modal title="About this survey" bind:open={menu} size="lg" outsideclose>
        <div>
          <P>{topView.title}: {topView.description}</P>
          Provided by: {topView.authors}
        </div>
        <div>This site lives in Github! Visit: {topView.addEntry.github}</div>

        <div>
          <P>Looking for more interactive surveys? Check out:</P>
          {#each surveys as survey}
            <Li><A href={survey.url}>{survey.name}</A></Li>
          {/each}
        </div>
      </Modal>

      <DarkMode btnClass="!p-1 border-0" style="color:var(--primary)" />
      
    </div>
  </Navbar>
</header>

