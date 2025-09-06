<script>
	import MultiCombo from "./multiCombo.svelte";
	import {
		Textarea,
		Button,
		FloatingLabelInput,
		Modal,
		Tooltip,
	} from "flowbite-svelte";
	import { copyText } from "svelte-copy";

	let stitle = "";
	let title = "";
	let authors = "";
	let bibtex = "";
	let year = 2024;
	let doi = "";
	let json = "";
	export let detailView = [];
	export let freq = {};
	export let addEntryInfo;
	let categories = [];

	detailView.forEach((cate) => {
		if (cate in freq) {
			const temp = { name: cate, value: [] };
			let items = [];
			Object.keys(freq[cate]).forEach((prop) => {
				items.push({ value: prop, label: prop });
			});
			temp["choices"] = items;
			categories.push(temp);
		} else {
			categories.push({ name: cate, value: "" });
		}
	});

	const reset = () => {
		stitle = "";
		title = "";
		authors = "";
		bibtex = "";
		year = 2024;
		doi = "";
		json = "";
		categories.forEach((cate) => {
			if (Array.isArray(cate.value)) {
				cate.value = [];
			} else {
				cate.value = "";
			}
		});
	};

	const generateJson = () => {
		const paper = {
			shortTitle: stitle,
			title: title,
			authors: authors,
			bibtex: bibtex,
			year: year,
		};
		categories.forEach((cate) => {
			if (Array.isArray(cate.value)) {
				let lst = [];
				cate.value.forEach((entry) => {
					lst.push(entry.value);
				});
				paper[cate.name] = lst;
			} else {
				paper[cate.name] = cate.value;
			}
		});
		json = JSON.stringify(paper);
	};

	const updateCategory = (res) => {
		categories.forEach((cate) => {
			if (cate.name === res.detail.name) {
				cate.value = res.detail.prop;
				return;
			}
		});
		generateJson();
	};
</script>

{#each addEntryInfo.description as para}
	{para} <br />
{/each}
Please feel free to open a Github issue if you wish to update an entry as well!

<div class="entry-content">
	<div class="entry-row">
		<div class="title-text"><strong>Title:</strong></div>
		<div class="text-field">
			<FloatingLabelInput
				size="small"
				style="outlined"
				id="title"
				name="title"
				on:change={generateJson}
				bind:value={title}
				type="text"
			>
				e.g., Longest Title of a Paper: The Story
			</FloatingLabelInput>
		</div>
	</div>
	<div class="entry-row">
		<div class="title-text"><strong>Year:</strong></div>
		<div class="text-field">
			<FloatingLabelInput
				size="small"
				style="outlined"
				id="year"
				name="year"
				on:change={generateJson}
				bind:value={year}
				type="text"
			>
				e.g., 2023
			</FloatingLabelInput>
		</div>
	</div>
	<div class="entry-row">
		<div class="title-text"><strong>Authors:</strong></div>
		<div class="text-field">
			<FloatingLabelInput
				size="small"
				style="outlined"
				id="authors"
				name="authors"
				on:change={generateJson}
				bind:value={authors}
				type="text"
			>
				e.g., John Doe, Jane Doe, Jack Doe
			</FloatingLabelInput>
		</div>
	</div>
	<div class="entry-row">
		<div class="title-text"><strong>Categories:</strong></div>
		<div class="catagory-field">
			{#each categories as category}
				<div class="title-cate">
					<strong>{category.name}:</strong>
					{#if "choices" in category}
						<MultiCombo
							items={category.choices}
							name={category.name}
							on:message={updateCategory}
						/>
					{:else}
						<Textarea
							style="width: 100%; height:40px"
							rows="2"
							on:change={generateJson}
							bind:value={category.value}
							placeholder={category.label}
						/>
					{/if}
				</div>
			{/each}
		</div>
	</div>
	<div class="entry-row">
		<div class="title-text"><strong>BibTex:</strong></div>
		<Textarea
			style="width: 100%;"
			rows="2"
			on:change={generateJson}
			bind:value={bibtex}
			placeholder="copy and paste bibtex"
		/>
	</div>
	<div class="entry-row">
		<div class="title-text"><strong>DOI:</strong></div>
		<div class="text-field">
			<FloatingLabelInput
				size="small"
				style="outlined"
				id="doi"
				name="doi"
				on:change={generateJson}
				bind:value={doi}
				type="text"
			>
				e.g., "https://doi.org/10..." or just the "10..." part.
			</FloatingLabelInput>
		</div>
	</div>
</div>
<div style="display:flex; justify-content:space-between; ">
	<div>
		<Button id="resetForm" on:click={reset}>Reset</Button>

		<Tooltip
			trigger="click"
			triggeredBy={"#resetForm"}
			placement="right">Form reset
		</Tooltip>
	</div>
	<div>
		<Button id="copyJson"
			on:click={() => {
				copyText(json);
			}}
		>
			Copy to Clipboard
		</Button>
		
		<Tooltip
			trigger="click"
			triggeredBy={"#copyJson"}
			placement="left">Copied JSON to clipboard!
		</Tooltip>
		{#if addEntryInfo.github}
			<Button
				on:click={() => window.open(addEntryInfo.github + '/issues/new', "_blank")}
			>
				Open Issue
			</Button>
		{:else if addEntryInfo.email}
			<Button
				on:click={() => window.open(addEntryInfo.email, "_blank")}
			>
				Open email
			</Button>
		{/if}

	</div>
</div>

<style>
	.title-cate {
		padding: 5px 10px;
	}
	.catagory-field {
		height: 300px;
		width: 100%;
		border-radius: 5px;
		overflow-y: scroll;
	}
	.title-text {
		width: 100px;
		text-align: right;
		padding-right: 10px;
	}
	.entry-row {
		display: flex;
		flex-direction: row;
		padding: 10px 10px 10px 0px;
		align-items: center;
		width: 100%;
	}
	.text-field {
		width: 100%;
		height: 40px;
	}
</style>
