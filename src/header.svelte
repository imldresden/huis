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
        id="about"
        on:click={() => (menu = true)}
      >
        <QuestionCircleOutline />
        <Tooltip triggeredBy="#about" placement="bottom">About</Tooltip>
      </Button>

      <Modal title="About this survey" bind:open={menu} size="lg" outsideclose>
        <div>
          <P>{topView.title}: {topView.description}</P>
              
            {#if (topView.authors.length === 1)}
              Author: <A href={topView.authors[0].orcid}>{topView.authors[0].name}</A>.
            {/if}
            {#if (topView.authors.length > 1)}
              Authors:{#each topView.authors.filter((_, i) => i < (topView.authors.length - 1)) as author}
                &nbsp;<A href={author.orcid}>{author.name}</A>,
              {/each}
              and <A href={topView.authors[topView.authors.length - 1].orcid}>{topView.authors[topView.authors.length - 1].name}</A>. 
            {/if}
        </div>
        
        
        <div>
          <P>Contact</P>
          <div>This site lives in Github! Visit: <A href={topView.addEntry.github}>{topView.addEntry.github}</A>, maintained by <A href={topView.site.contact}>{topView.site.maintainer}</A>.</div>
        </div>

        <div>
          <P>How to cite: </P>
          {topView.site["how-to"]} {#if (topView.site.doi)} <A href={topView.site.doi}>{topView.site.doi}</A> {/if}
          {#if (topView.site.bib)}, or this .bib entry: 
          <pre style="white-space: break-spaces;padding-top:30px">
{topView.site.bib[0]}
{#each topView.site.bib.filter((_,i) => i !== 0 && i !== topView.site.bib.length - 1) as bib, i}
&nbsp;&nbsp;{bib}{#if (i < topView.site.bib.length - 3)}<br />{/if}
{/each}
{topView.site.bib[topView.site.bib.length - 1]}
          </pre>
          {/if}
        </div>

        <div>
          <P>Looking for more interactive surveys? Check out:</P>
          <ul>
            {#each surveys as survey}
              <Li><A href={survey.url}>{survey.name}</A></Li>
            {/each}
          </ul>
        </div>
      </Modal>

      <DarkMode btnClass="!p-1 border-0" style="color:var(--primary)" />
      
    </div>
  </Navbar>
</header>

