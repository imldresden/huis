<script>
  import { Tooltip, Button, P } from "flowbite-svelte";
  import { AccordionItem, Accordion } from "flowbite-svelte";
  import { CogOutline  } from "flowbite-svelte-icons";
  import StackGraph from "./vis/stackGraph.svelte";
  import CorrMetric from "./vis/corrMetric.svelte";
  import { filterBy } from "./store";
  export let data;
  
  let width;
  let choicesDim = [];

  //Get the list of dimension to visualize
  $filterBy.forEach((prop, i) => {
    //This contains two levels of grouping
    if ("groupName" in prop) {
      choicesDim.push({ name: prop.groupName, index: i });
    } else {
      //One level deep
      choicesDim.push({ name: prop.name, index: i });
    }
  });
  $: selectedDimX = choicesDim[0];
  $: selectedDimY = choicesDim[1];
  $: selectedCate = choicesDim[0];
  $: selectedSubCate = choicesDim[0];
  $: subCates = [];
  $: if ("groupName" in $filterBy[selectedCate.index]) {
    subCates = [];
    subCates.push("All");
    $filterBy[selectedCate.index].categories.forEach((cate) => {
      subCates.push(cate.name);
    });
    selectedSubCate = "All";
  } else {
    selectedSubCate = selectedCate;
  }

  $: showHideSettings = (which) => {
    Array.from(document.getElementsByClassName(which)).forEach((el) => {
        el.classList.toggle("hidden")
    })
  }

</script>
<svelte:window bind:innerWidth={width} />

<div class="vis-panel dark:bg-gray-900">
  <Accordion>
    <AccordionItem open={true}>
      <div slot="header" style="display:flex">Correlation Matrix 
        <Button
          pill={true}
          outline
          class="!p-1 border-0"
          id="about"
          on:click={(eve) =>  {
              eve.stopPropagation();
              showHideSettings("corr-hidable");
            }}
        >
          <CogOutline />
          <Tooltip placement="bottom">Settings</Tooltip>
        </Button>

      </div>
      
      <div class="flexy">
        <div class="flex flex-wrap space-x-1 pb-3 items-center corr-hidable hidden">
          <P style="padding-left:20px">X-Axis:</P>
          {#each choicesDim as dim}
            <Button
              size="sm"
              outline
              class="p-1 {dim.name === selectedDimX.name
                ? 'dark:bg-gray-400 dark:text-primary-200'
                : 'cursor-pointer'}"
              on:click={() => {
                selectedDimX = dim;
              }}>{dim.name}</Button
            >
          {/each}
        </div>

        <div class="flex flex-wrap space-x-1 items-center corr-hidable hidden">
          <P style="padding-left:20px">Y-Axis:</P>
          {#each choicesDim as dim}
            <Button
              outline
              size="sm"
              class="p-1 {dim.name === selectedDimY.name
                ? 'dark:bg-gray-400 dark:text-primary-200'
                : 'cursor-pointer'}"
              on:click={() => {
                selectedDimY = dim;
              }}>{dim.name}</Button
            >
          {/each}
        </div>
      </div>

      <!-- Create the visualization -->
      <CorrMetric
        {data}
        selectedDimX={selectedDimX.name}
        selectedDimY={selectedDimY.name}
        on:message
      />
    </AccordionItem>
    <AccordionItem>
      <div slot="header" style="display:flex">Over the Years
      <Button
          pill={true}
          outline
          class="!p-1 border-0"
          id="about"
          on:click={(eve) =>  {
              eve.stopPropagation();
              showHideSettings("stack-hidable");
            }}
        >
          <CogOutline />
          <Tooltip placement="bottom">Settings</Tooltip>
        </Button>

      </div>

      <div class="flexy">
        <div class="stack-hidable hidden"> 
          <div class="flex flex-wrap space-x-1 pb-3 items-center">
            <P style="padding-left:20px">Categories:</P>
            {#each choicesDim as dim}
              <Button
                size="sm"
                outline
                class="p-1 {dim.name === selectedCate.name
                  ? 'dark:bg-gray-400 dark:text-primary-200'
                  : 'cursor-pointer'}"
                on:click={() => {
                  selectedCate = dim;
                }}>{dim.name}</Button
              >
            {/each}
          </div>
          {#if subCates.length > 0}
            <div class="flex flex-wrap space-x-1 pb-3 items-center">
              <P style="padding-left:20px">Sub-Categories:</P>
              {#each subCates as subcate}
                <Button
                  size="sm"
                  outline
                  class="p-1 {subcate === selectedSubCate
                    ? 'dark:bg-gray-400 dark:text-primary-200'
                    : 'cursor-pointer'}"
                  on:click={() => {
                    selectedSubCate = subcate;
                  }}>{subcate}</Button
                >
              {/each}
            </div>
          {/if}
        </div>
        
        <StackGraph
          {data}
          selectedCate={selectedSubCate === "All"
            ? selectedCate.name
            : selectedSubCate}
          on:message
        />
      </div>
    </AccordionItem>
  </Accordion>
</div>

<style>
  .vis-panel {
    padding: 10px 5px;
    height: 100%;
    width: 100%;
  }
  .hidden {
    display: none
  }
</style>
