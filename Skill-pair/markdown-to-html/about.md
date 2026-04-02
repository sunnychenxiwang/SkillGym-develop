



<!DOCTYPE html>
<html class="gl-system ui-neutral with-top-bar with-header application-chrome page-with-panels with-gl-container-queries" lang="en">
<head prefix="og: http://ogp.me/ns#">
<meta charset="utf-8">
<meta content="IE=edge" http-equiv="X-UA-Compatible">
<meta content="width=device-width, initial-scale=1" name="viewport">
<title>_pages/about.md · master · Ali Hashemi / AliHashemi-github-io · GitLab</title>
<script>
//<![CDATA[
window.gon={};gon.math_rendering_limits_enabled=true;gon.features={"allowIframesInMarkdown":false,"inlineBlame":false,"repositoryFileTreeBrowser":true,"blobEditRefactor":true,"repositoryLockInformation":false,"convertToGlCiFlowRegistry":true};gon.licensed_features={"remoteDevelopment":false};
//]]>
</script>

<script>
//<![CDATA[
const root = document.documentElement;
if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
  root.classList.add('gl-dark');
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  if (e.matches) {
    root.classList.add('gl-dark');
  } else {
    root.classList.remove('gl-dark');
  }
});

//]]>
</script>
<script>
//<![CDATA[
var gl = window.gl || {};
gl.startup_calls = {"/hashemi/AliHashemi-github-io/-/blob/master/_pages/about.md?format=json\u0026viewer=rich":{}};
gl.startup_graphql_calls = [{"query":"# @feature_category: source_code_management\nquery getBlobInfo(\n  $projectPath: ID!\n  $filePath: [String!]!\n  $ref: String!\n  $refType: RefType\n  $shouldFetchRawText: Boolean!\n) {\n  project(fullPath: $projectPath) {\n    __typename\n    id\n    repository {\n      __typename\n      empty\n      blobs(paths: $filePath, ref: $ref, refType: $refType) {\n        __typename\n        nodes {\n          __typename\n          id\n          webPath\n          name\n          size\n          rawSize\n          rawTextBlob @include(if: $shouldFetchRawText)\n          fileType\n          language\n          path\n          blamePath\n          editBlobPath\n          gitpodBlobUrl\n          ideEditPath\n          forkAndEditPath\n          ideForkAndEditPath\n          codeNavigationPath\n          projectBlobPathRoot\n          forkAndViewPath\n          environmentFormattedExternalUrl\n          environmentExternalUrlForRouteMap\n          canModifyBlob\n          canModifyBlobWithWebIde\n          canCurrentUserPushToBranch\n          archived\n          storedExternally\n          externalStorage\n          externalStorageUrl\n          rawPath\n          replacePath\n          pipelineEditorPath\n          simpleViewer {\n            fileType\n            tooLarge\n            type\n            renderError\n          }\n          richViewer {\n            fileType\n            tooLarge\n            type\n            renderError\n          }\n        }\n      }\n    }\n  }\n}\n","variables":{"projectPath":"hashemi/AliHashemi-github-io","ref":"master","refType":"HEADS","filePath":"_pages/about.md","shouldFetchRawText":false}}];

if (gl.startup_calls && window.fetch) {
  Object.keys(gl.startup_calls).forEach(apiCall => {
   gl.startup_calls[apiCall] = {
      fetchCall: fetch(apiCall, {
        // Emulate XHR for Rails AJAX request checks
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        },
        // fetch won’t send cookies in older browsers, unless you set the credentials init option.
        // We set to `same-origin` which is default value in modern browsers.
        // See https://github.com/whatwg/fetch/pull/585 for more information.
        credentials: 'same-origin'
      })
    };
  });
}
if (gl.startup_graphql_calls && window.fetch) {
  const headers = {"X-CSRF-Token":"C1Wq9s6Fdn5NGg3y69VzYBZhLViexm695OOeA__Df5EDjYCierk2VevJbsnOi4NFjwtIrLW0_E6a5uQQC2e67w","x-gitlab-feature-category":"source_code_management"};
  const url = `https://git.tu-berlin.de/api/graphql`

  const opts = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...headers,
    }
  };

  gl.startup_graphql_calls = gl.startup_graphql_calls.map(call => ({
    ...call,
    fetchCall: fetch(url, {
      ...opts,
      credentials: 'same-origin',
      body: JSON.stringify(call)
    })
  }))
}


//]]>
</script>

<link rel="prefetch" href="/assets/webpack/monaco.2f50fc5f.chunk.js">

<meta content="light dark" name="color-scheme">
<link rel="stylesheet" href="/assets/application-9e8889e3cef31f1127573c849241a8e0dcc71180500f636d991775331e5f888b.css" media="(prefers-color-scheme: light)" />
<link rel="stylesheet" href="/assets/application_dark-356d95c4fa890d9f5f361b90ec62bfe31462684c92c1ae4a227b21c27347b045.css" media="(prefers-color-scheme: dark)" />
<link rel="stylesheet" href="/assets/page_bundles/tree-fb7df91c595e3158c2ad5a485cfb0039d488d3ba8e39d62b61cd585c78608e64.css" /><link rel="stylesheet" href="/assets/page_bundles/projects-1e46068245452053a00290f44a0ebda348b43ba90e413a07b9d36767e72b79aa.css" /><link rel="stylesheet" href="/assets/page_bundles/commit_description-9e7efe20f0cef17d0606edabfad0418e9eb224aaeaa2dae32c817060fa60abcc.css" /><link rel="stylesheet" href="/assets/page_bundles/work_items-af321897c3b1ae7c1f6f0cb993681211b837df7ec8e5ff59e3795fd08ab83a13.css" /><link rel="stylesheet" href="/assets/page_bundles/notes_shared-8f7a9513332533cc4a53b3be3d16e69570e82bc87b3f8913578eaeb0dce57e21.css" />
<link rel="stylesheet" href="/assets/tailwind_cqs-d51dc05c8c0696a511881802ecd259633fbabf6608e57c39e367821db8c4ad01.css" />


<link rel="stylesheet" href="/assets/fonts-deb7ad1d55ca77c0172d8538d53442af63604ff490c74acc2859db295c125bdb.css" />
<link rel="stylesheet" href="/assets/highlight/themes/white-9c3096bebbc271536c91d4e96afdef34cf54f198accca96d32008405a3a398da.css" media="(prefers-color-scheme: light)" />
<link rel="stylesheet" href="/assets/highlight/themes/dark-bab508e186c8119f0cfb965d3a8a74c6ee2b10c5d2cf129a41c0bc522b98655d.css" media="(prefers-color-scheme: dark)" />

<script src="/assets/webpack/runtime.2294e646.bundle.js" defer="defer"></script>
<script src="/assets/webpack/main.ea08bfa6.chunk.js" defer="defer"></script>
<script src="/assets/webpack/tracker.f99708a3.chunk.js" defer="defer"></script>
<script>
//<![CDATA[
window.snowplowOptions = {"namespace":"gl","hostname":"git.tu-berlin.de:443","postPath":"/-/collect_events","forceSecureTracker":true,"appId":"gitlab_sm"};
gl = window.gl || {};
gl.snowplowStandardContext = {"schema":"iglu:com.gitlab/gitlab_standard/jsonschema/1-1-7","data":{"environment":"self-managed","source":"gitlab-rails","correlation_id":"01KN5RGG93JG691JZ5H1FFXAAV","extra":{},"user_id":null,"global_user_id":null,"user_type":null,"is_gitlab_team_member":null,"namespace_id":35607,"ultimate_parent_namespace_id":35607,"project_id":23753,"feature_enabled_by_namespace_ids":null,"realm":"self-managed","deployment_type":"self-managed","context_generated_at":"2026-04-02T00:11:54.374Z"}};
gl.snowplowPseudonymizedPageUrl = "https://git.tu-berlin.de/namespace35607/project23753/-/blob/:repository_path";
gl.maskedDefaultReferrerUrl = null;
gl.ga4MeasurementId = 'G-ENFH3X7M5Y';
gl.duoEvents = ["ai_question_category","perform_completion_worker","process_gitlab_duo_question","agent_platform_session_created","agent_platform_session_dropped","agent_platform_session_finished","agent_platform_session_resumed","agent_platform_session_started","agent_platform_session_stopped","ai_response_time","ci_repository_xray_artifact_created","cleanup_stuck_agent_platform_session","click_dap_trial_or_paid_empty_state_agent","click_dap_trial_or_paid_empty_state_explore_agents_link","click_dap_trial_or_paid_empty_state_prompt","click_delete_ai_catalog_item_button","click_disable_ai_catalog_item_button","click_duo_agentic_not_available_empty_state_learn_more","click_duo_agentic_not_available_empty_state_start_trial","click_duplicate_ai_catalog_item_button","click_enable_ai_catalog_item_button","click_purchase_seats_button_group_duo_pro_home_page","code_suggestion_accepted_in_ide","code_suggestion_rejected_in_ide","code_suggestion_shown_in_ide","code_suggestions_connection_details_rate_limit_exceeded","code_suggestions_direct_access_rate_limit_exceeded","code_suggestions_rate_limit_exceeded","create_ai_catalog_item","create_ai_catalog_item_consumer","create_ai_self_hosted_model","default_answer","delete_ai_catalog_item","delete_ai_catalog_item_consumer","delete_ai_self_hosted_model","detected_high_comment_temperature","detected_repeated_high_comment_temperature","dismiss_sast_vulnerability_false_positive_analysis","encounter_duo_code_review_error_during_review","error_answer","excluded_files_from_duo_code_review","execute_llm_method","filter_ai_fp","find_no_issues_duo_code_review_after_review","find_nothing_to_review_duo_code_review_on_mr","finish_duo_workflow_execution","finish_mcp_tool_call","forced_high_temperature_commenting","i_quickactions_q","include_repository_xray_data_into_code_generation_prompt","mention_gitlabduo_in_mr_comment","post_comment_duo_code_review_on_diff","process_gitlab_duo_slash_command","react_thumbs_down_on_duo_code_review_comment","react_thumbs_up_on_duo_code_review_comment","reported_sast_vulnerability_false_positive_analysis","request_ask_help","request_duo_chat_response","request_review_duo_code_review_on_mr_by_author","request_review_duo_code_review_on_mr_by_non_author","requested_comment_temperature","retry_duo_workflow_execution","start_duo_workflow_execution","start_mcp_tool_call","submit_gitlab_duo_question","tokens_per_embedding","tokens_per_user_request_prompt","tokens_per_user_request_response","trigger_ai_catalog_item","trigger_sast_vulnerability_fp_detection_workflow","trigger_sast_vulnerability_resolution_workflow","trigger_secret_detection_vulnerability_fp_detection_workflow","troubleshoot_job","update_ai_catalog_item","update_ai_catalog_item_consumer","update_ai_self_hosted_model","update_model_selection_feature","update_self_hosted_ai_feature_to_vendored_model","view_ai_catalog_item","view_ai_catalog_item_index","view_ai_catalog_project_managed","view_dap_trial_or_paid_empty_state","view_duo_agentic_not_available_empty_state"];
gl.onlySendDuoEvents = true;


//]]>
</script>
<link rel="preload" href="/assets/application-9e8889e3cef31f1127573c849241a8e0dcc71180500f636d991775331e5f888b.css" as="style" type="text/css">
<link rel="preload" href="/assets/highlight/themes/white-9c3096bebbc271536c91d4e96afdef34cf54f198accca96d32008405a3a398da.css" as="style" type="text/css">




<script src="/assets/webpack/commons-pages.search.show-super_sidebar.859fa515.chunk.js" defer="defer"></script>
<script src="/assets/webpack/super_sidebar.a2ef804f.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.groups-pages.groups.achievements-pages.groups.activity-pages.groups.analytics.ci_cd_an-6751a3a9.e7669245.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.groups.epics.index-pages.groups.epics.new-pages.groups.epics.show-pages.groups.issues--a711c0bb.0327aa1b.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.edit-pages.projects.blob.new-pages.projects.blob.show-pages.projects.get-487ddc08.5084395a.chunk.js" defer="defer"></script>
<script src="/assets/webpack/467359d4.8ad0411d.chunk.js" defer="defer"></script>
<script src="/assets/webpack/ea7ea8c3.58ef5d7f.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.show-pages.projects.snippets.show-pages.projects.tre-c684fcf6.d82547ff.chunk.js" defer="defer"></script>
<script src="/assets/webpack/35610df2.df98942d.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.commits.show-pages.projects.show-pages.projects.tree.show.81b29c30.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blame.show-pages.projects.blob.show-pages.projects.show-pages.projects.tree.show.bd918edf.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.groups.show-pages.projects.blob.show-pages.projects.show-pages.projects.tree.show.24f7ea52.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.show-pages.projects.tree.show.ac4473ab.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.tree.show-treeList.85ad02e2.chunk.js" defer="defer"></script>
<script src="/assets/webpack/pages.projects.blob.show.442669b5.chunk.js" defer="defer"></script>

<meta content="object" property="og:type">
<meta content="GitLab" property="og:site_name">
<meta content="_pages/about.md · master · Ali Hashemi / AliHashemi-github-io · GitLab" property="og:title">
<meta content="Github Pages template for academic personal websites, forked from mmistakes/minimal-mistakes" property="og:description">
<meta content="https://git.tu-berlin.de/assets/twitter_card-570ddb06edf56a2312253c5872489847a0f385112ddbcd71ccfa1570febab5d2.jpg" property="og:image">
<meta content="64" property="og:image:width">
<meta content="64" property="og:image:height">
<meta content="https://git.tu-berlin.de/hashemi/AliHashemi-github-io/-/blob/master/_pages/about.md" property="og:url">
<meta content="summary" property="twitter:card">
<meta content="_pages/about.md · master · Ali Hashemi / AliHashemi-github-io · GitLab" property="twitter:title">
<meta content="Github Pages template for academic personal websites, forked from mmistakes/minimal-mistakes" property="twitter:description">
<meta content="https://git.tu-berlin.de/assets/twitter_card-570ddb06edf56a2312253c5872489847a0f385112ddbcd71ccfa1570febab5d2.jpg" property="twitter:image">

<meta name="csrf-param" content="authenticity_token" />
<meta name="csrf-token" content="uDS0M2Hf4471Wqy1Aq1Uh-ozpZY_61_h-EmtSp3eY_iw7J5n1eOjpVOJz44n86Sic1nAYhSZzRKGTNdZaXqmhg" />
<meta name="csp-nonce" />
<meta name="action-cable-url" content="/-/cable" />
<link href="/-/manifest.json" rel="manifest">
<link rel="icon" type="image/png" href="/assets/favicon-72a2cad5025aa931d6ea56c3201d1f18e68a8cd39788c7c80d5b2b82aa5143ef.png" id="favicon" data-original-href="/assets/favicon-72a2cad5025aa931d6ea56c3201d1f18e68a8cd39788c7c80d5b2b82aa5143ef.png" />
<link rel="apple-touch-icon" type="image/x-icon" href="/assets/apple-touch-icon-b049d4bc0dd9626f31db825d61880737befc7835982586d015bded10b4435460.png" />
<link href="/search/opensearch.xml" rel="search" title="Search GitLab" type="application/opensearchdescription+xml">




<meta content="Github Pages template for academic personal websites, forked from mmistakes/minimal-mistakes" name="description">
<meta content="#F1F0F6" media="(prefers-color-scheme: light)" name="theme-color">
<meta content="#232128" media="(prefers-color-scheme: dark)" name="theme-color">
</head>

<body class="tab-width-8 gl-browser-generic gl-platform-other" data-namespace-id="35607" data-page="projects:blob:show" data-page-type-id="master/_pages/about.md" data-project="AliHashemi-github-io" data-project-full-path="hashemi/AliHashemi-github-io" data-project-id="23753" data-project-studio-enabled="true">
<div id="js-tooltips-container"></div>

<script>
//<![CDATA[
gl = window.gl || {};
gl.client = {"isGeneric":true,"isOther":true};


//]]>
</script>


<header class="super-topbar js-super-topbar"></header>
<div class="layout-page js-page-layout page-with-super-sidebar">
<script>
//<![CDATA[
const outer = document.createElement('div');
outer.style.visibility = 'hidden';
outer.style.overflow = 'scroll';
document.body.appendChild(outer);
const inner = document.createElement('div');
outer.appendChild(inner);
const scrollbarWidth = outer.offsetWidth - inner.offsetWidth;
outer.parentNode.removeChild(outer);
document.documentElement.style.setProperty('--scrollbar-width', `${scrollbarWidth}px`);

//]]>
</script><aside class="js-super-sidebar super-sidebar super-sidebar-loading" data-command-palette="{&quot;project_files_url&quot;:&quot;/hashemi/AliHashemi-github-io/-/files/master?format=json&quot;,&quot;project_blob_url&quot;:&quot;/hashemi/AliHashemi-github-io/-/blob/master&quot;}" data-is-saas="false" data-root-path="/" data-sidebar="{&quot;is_logged_in&quot;:false,&quot;compare_plans_url&quot;:&quot;https://about.gitlab.com/pricing&quot;,&quot;context_switcher_links&quot;:[{&quot;title&quot;:&quot;Explore&quot;,&quot;link&quot;:&quot;/explore&quot;,&quot;icon&quot;:&quot;compass&quot;}],&quot;current_menu_items&quot;:[{&quot;id&quot;:&quot;project_overview&quot;,&quot;title&quot;:&quot;AliHashemi-github-io&quot;,&quot;entity_id&quot;:23753,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io&quot;,&quot;link_classes&quot;:&quot;shortcuts-project&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;manage_menu&quot;,&quot;title&quot;:&quot;Manage&quot;,&quot;icon&quot;:&quot;users&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/activity&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;activity&quot;,&quot;title&quot;:&quot;Activity&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/activity&quot;,&quot;link_classes&quot;:&quot;shortcuts-project-activity&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;members&quot;,&quot;title&quot;:&quot;Members&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/project_members&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;labels&quot;,&quot;title&quot;:&quot;Labels&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/labels&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;plan_menu&quot;,&quot;title&quot;:&quot;Plan&quot;,&quot;icon&quot;:&quot;planning&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/issues&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;project_issue_list&quot;,&quot;title&quot;:&quot;Issues&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/issues&quot;,&quot;link_classes&quot;:&quot;shortcuts-issues has-sub-items&quot;,&quot;pill_count_field&quot;:&quot;openIssuesCount&quot;,&quot;pill_count_dynamic&quot;:false,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;boards&quot;,&quot;title&quot;:&quot;Issue boards&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/boards&quot;,&quot;link_classes&quot;:&quot;shortcuts-issue-boards&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;milestones&quot;,&quot;title&quot;:&quot;Milestones&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/milestones&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;project_wiki&quot;,&quot;title&quot;:&quot;Wiki&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/wikis/home&quot;,&quot;link_classes&quot;:&quot;shortcuts-wiki&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;code_menu&quot;,&quot;title&quot;:&quot;Code&quot;,&quot;icon&quot;:&quot;code&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/merge_requests&quot;,&quot;is_active&quot;:true,&quot;items&quot;:[{&quot;id&quot;:&quot;project_merge_request_list&quot;,&quot;title&quot;:&quot;Merge requests&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/merge_requests&quot;,&quot;link_classes&quot;:&quot;shortcuts-merge_requests&quot;,&quot;pill_count_field&quot;:&quot;openMergeRequestsCount&quot;,&quot;pill_count_dynamic&quot;:false,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;files&quot;,&quot;title&quot;:&quot;Repository&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/tree/master&quot;,&quot;link_classes&quot;:&quot;shortcuts-tree&quot;,&quot;is_active&quot;:true},{&quot;id&quot;:&quot;branches&quot;,&quot;title&quot;:&quot;Branches&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/branches&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;commits&quot;,&quot;title&quot;:&quot;Commits&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/commits/master?ref_type=heads&quot;,&quot;link_classes&quot;:&quot;shortcuts-commits&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;tags&quot;,&quot;title&quot;:&quot;Tags&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/tags&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;graphs&quot;,&quot;title&quot;:&quot;Repository graph&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/network/master?ref_type=heads&quot;,&quot;link_classes&quot;:&quot;shortcuts-network&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;compare&quot;,&quot;title&quot;:&quot;Compare revisions&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/compare?from=master\u0026to=master&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;project_snippets&quot;,&quot;title&quot;:&quot;Snippets&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/snippets&quot;,&quot;link_classes&quot;:&quot;shortcuts-snippets&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;build_menu&quot;,&quot;title&quot;:&quot;Build&quot;,&quot;icon&quot;:&quot;rocket&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/pipelines&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;pipelines&quot;,&quot;title&quot;:&quot;Pipelines&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/pipelines&quot;,&quot;link_classes&quot;:&quot;shortcuts-pipelines&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;jobs&quot;,&quot;title&quot;:&quot;Jobs&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/jobs&quot;,&quot;link_classes&quot;:&quot;shortcuts-builds&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;pipeline_schedules&quot;,&quot;title&quot;:&quot;Pipeline schedules&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/pipeline_schedules&quot;,&quot;link_classes&quot;:&quot;shortcuts-builds&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;artifacts&quot;,&quot;title&quot;:&quot;Artifacts&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/artifacts&quot;,&quot;link_classes&quot;:&quot;shortcuts-builds&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;deploy_menu&quot;,&quot;title&quot;:&quot;Deploy&quot;,&quot;icon&quot;:&quot;deployments&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/releases&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;releases&quot;,&quot;title&quot;:&quot;Releases&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/releases&quot;,&quot;link_classes&quot;:&quot;shortcuts-deployments-releases&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;packages_registry&quot;,&quot;title&quot;:&quot;Package registry&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/packages&quot;,&quot;link_classes&quot;:&quot;shortcuts-container-registry&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;container_registry&quot;,&quot;title&quot;:&quot;Container registry&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/container_registry&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;model_registry&quot;,&quot;title&quot;:&quot;Model registry&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/ml/models&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;operations_menu&quot;,&quot;title&quot;:&quot;Operate&quot;,&quot;icon&quot;:&quot;cloud-pod&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/environments&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;environments&quot;,&quot;title&quot;:&quot;Environments&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/environments&quot;,&quot;link_classes&quot;:&quot;shortcuts-environments&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;infrastructure_registry&quot;,&quot;title&quot;:&quot;Terraform modules&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/terraform_module_registry&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;monitor_menu&quot;,&quot;title&quot;:&quot;Monitor&quot;,&quot;icon&quot;:&quot;monitor&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/incidents&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;incidents&quot;,&quot;title&quot;:&quot;Incidents&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/incidents&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;analyze_menu&quot;,&quot;title&quot;:&quot;Analyze&quot;,&quot;icon&quot;:&quot;chart&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/value_stream_analytics&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;cycle_analytics&quot;,&quot;title&quot;:&quot;Value stream analytics&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/value_stream_analytics&quot;,&quot;link_classes&quot;:&quot;shortcuts-project-cycle-analytics&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;contributors&quot;,&quot;title&quot;:&quot;Contributor analytics&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/graphs/master?ref_type=heads&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;ci_cd_analytics&quot;,&quot;title&quot;:&quot;CI/CD analytics&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/pipelines/charts&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;repository_analytics&quot;,&quot;title&quot;:&quot;Repository analytics&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/graphs/master/charts&quot;,&quot;link_classes&quot;:&quot;shortcuts-repository-charts&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;issues&quot;,&quot;title&quot;:&quot;Issue analytics&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/analytics/issues_analytics&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;model_experiments&quot;,&quot;title&quot;:&quot;Model experiments&quot;,&quot;link&quot;:&quot;/hashemi/AliHashemi-github-io/-/ml/experiments&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false}],&quot;current_context_header&quot;:&quot;Project&quot;,&quot;university_path&quot;:&quot;https://university.gitlab.com&quot;,&quot;support_path&quot;:&quot;https://support.gitlab.com&quot;,&quot;docs_path&quot;:&quot;/help/docs&quot;,&quot;display_whats_new&quot;:false,&quot;show_version_check&quot;:null,&quot;search&quot;:{&quot;search_path&quot;:&quot;/search&quot;,&quot;issues_path&quot;:&quot;/dashboard/issues&quot;,&quot;mr_path&quot;:&quot;/dashboard/merge_requests&quot;,&quot;autocomplete_path&quot;:&quot;/search/autocomplete&quot;,&quot;settings_path&quot;:&quot;/search/settings&quot;,&quot;search_context&quot;:{&quot;project&quot;:{&quot;id&quot;:23753,&quot;name&quot;:&quot;AliHashemi-github-io&quot;},&quot;project_metadata&quot;:{&quot;mr_path&quot;:&quot;/hashemi/AliHashemi-github-io/-/merge_requests&quot;,&quot;issues_path&quot;:&quot;/hashemi/AliHashemi-github-io/-/issues&quot;},&quot;code_search&quot;:true,&quot;ref&quot;:&quot;master&quot;,&quot;scope&quot;:null,&quot;for_snippets&quot;:null}},&quot;panel_type&quot;:&quot;project&quot;,&quot;shortcut_links&quot;:[{&quot;title&quot;:&quot;Snippets&quot;,&quot;href&quot;:&quot;/explore/snippets&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-snippets&quot;},{&quot;title&quot;:&quot;Groups&quot;,&quot;href&quot;:&quot;/explore/groups&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-groups&quot;},{&quot;title&quot;:&quot;Projects&quot;,&quot;href&quot;:&quot;/explore/projects&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-projects&quot;}],&quot;terms&quot;:&quot;/-/users/terms&quot;,&quot;sign_in_visible&quot;:&quot;true&quot;,&quot;allow_signup&quot;:&quot;false&quot;,&quot;new_user_registration_path&quot;:&quot;/users/sign_up&quot;,&quot;sign_in_path&quot;:&quot;/users/sign_in?redirect_to_referer=yes&quot;}"></aside>

<div class="panels-container gl-flex gl-gap-3">
<div class="content-panels gl-flex-1 gl-w-full gl-flex gl-gap-3 gl-relative js-content-panels gl-@container/content-panels">
<div class="js-static-panel static-panel content-wrapper gl-relative paneled-view gl-flex-1 gl-overflow-y-auto gl-bg-default" id="static-panel-portal">
<div class="panel-header">
<div class="broadcast-wrapper">



</div>
<div class="top-bar-fixed container-fluid gl-rounded-t-lg gl-sticky gl-top-0 gl-left-0 gl-mx-0 gl-w-full" data-testid="top-bar">
<div class="top-bar-container gl-flex gl-items-center gl-gap-2">
<div class="gl-grow gl-basis-0 gl-flex gl-items-center gl-justify-start gl-gap-3">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Ali Hashemi","item":"https://git.tu-berlin.de/hashemi"},{"@type":"ListItem","position":2,"name":"AliHashemi-github-io","item":"https://git.tu-berlin.de/hashemi/AliHashemi-github-io"},{"@type":"ListItem","position":3,"name":"Repository","item":"https://git.tu-berlin.de/hashemi/AliHashemi-github-io/-/blob/master/_pages/about.md"}]}


</script>
<div data-testid="breadcrumb-links" id="js-vue-page-breadcrumbs-wrapper">
<div data-breadcrumbs-json="[{&quot;text&quot;:&quot;Ali Hashemi&quot;,&quot;href&quot;:&quot;/hashemi&quot;,&quot;avatarPath&quot;:null},{&quot;text&quot;:&quot;AliHashemi-github-io&quot;,&quot;href&quot;:&quot;/hashemi/AliHashemi-github-io&quot;,&quot;avatarPath&quot;:null},{&quot;text&quot;:&quot;Repository&quot;,&quot;href&quot;:&quot;/hashemi/AliHashemi-github-io/-/blob/master/_pages/about.md&quot;,&quot;avatarPath&quot;:null}]" id="js-vue-page-breadcrumbs"></div>
<div id="js-injected-page-breadcrumbs"></div>
<div id="js-page-breadcrumbs-extra"></div>
</div>


<div id="js-work-item-feedback"></div>

</div>
</div>
</div>

</div>
<div class="panel-content">
<div class="panel-content-inner js-static-panel-inner">
<div class="alert-wrapper alert-wrapper-top-space gl-flex gl-flex-col gl-gap-3 container-fluid container-limited">


























</div>

<div class="container-fluid container-limited project-highlight-puc">
<main class="content gl-@container/panel gl-pb-3" id="content-body" itemscope itemtype="http://schema.org/SoftwareSourceCode">
<div id="js-drawer-container"></div>
<div class="flash-container flash-container-page sticky" data-testid="flash-container">
<div id="js-global-alerts"></div>
</div>








<div class="js-signature-container" data-signatures-path="/hashemi/AliHashemi-github-io/-/commits/82450fc0612271dd703ff1bc532610aae337bdaf/signatures?limit=1"></div>

<div class="gl-flex navigation-root">
<div id="js-file-browser"></div>
<div class="tree-holder gl-pt-5 gl-pl-4 gl-w-full gl-min-w-0" id="tree-holder">
<div data-blob-path="_pages/about.md" data-breadcrumbs-can-collaborate="false" data-breadcrumbs-can-edit-tree="false" data-breadcrumbs-can-push-code="false" data-breadcrumbs-can-push-to-branch="false" data-breadcrumbs-new-blob-path="/hashemi/AliHashemi-github-io/-/new/master" data-breadcrumbs-new-branch-path="/hashemi/AliHashemi-github-io/-/branches/new" data-breadcrumbs-new-dir-path="/hashemi/AliHashemi-github-io/-/create_dir/master" data-breadcrumbs-new-tag-path="/hashemi/AliHashemi-github-io/-/tags/new" data-breadcrumbs-upload-path="/hashemi/AliHashemi-github-io/-/create/master" data-download-links="[{&quot;text&quot;:&quot;zip&quot;,&quot;path&quot;:&quot;/hashemi/AliHashemi-github-io/-/archive/master/AliHashemi-github-io-master.zip&quot;},{&quot;text&quot;:&quot;tar.gz&quot;,&quot;path&quot;:&quot;/hashemi/AliHashemi-github-io/-/archive/master/AliHashemi-github-io-master.tar.gz&quot;},{&quot;text&quot;:&quot;tar.bz2&quot;,&quot;path&quot;:&quot;/hashemi/AliHashemi-github-io/-/archive/master/AliHashemi-github-io-master.tar.bz2&quot;},{&quot;text&quot;:&quot;tar&quot;,&quot;path&quot;:&quot;/hashemi/AliHashemi-github-io/-/archive/master/AliHashemi-github-io-master.tar&quot;}]" data-escaped-ref="master" data-history-link="/hashemi/AliHashemi-github-io/-/commits/master" data-http-url="https://git.tu-berlin.de/hashemi/AliHashemi-github-io.git" data-new-workspace-path="/-/remote_development/workspaces/new" data-organization-id="1" data-project-id="23753" data-project-path="hashemi/AliHashemi-github-io" data-project-root-path="/hashemi/AliHashemi-github-io" data-project-short-path="AliHashemi-github-io" data-ref="master" data-ref-type="heads" data-root-ref="master" data-show-no-ssh-key-message="" data-ssh-url="git@git.tu-berlin.de:hashemi/AliHashemi-github-io.git" data-user-settings-ssh-keys-path="/-/user_settings/ssh_keys" data-web-ide-button-default-branch="master" data-web-ide-button-options="{&quot;project_path&quot;:&quot;hashemi/AliHashemi-github-io&quot;,&quot;ref&quot;:&quot;master&quot;,&quot;is_fork&quot;:false,&quot;needs_to_fork&quot;:true,&quot;gitpod_enabled&quot;:false,&quot;is_blob&quot;:true,&quot;show_edit_button&quot;:false,&quot;show_web_ide_button&quot;:false,&quot;show_gitpod_button&quot;:false,&quot;show_pipeline_editor_button&quot;:false,&quot;web_ide_url&quot;:&quot;/-/ide/project/hashemi/AliHashemi-github-io/edit/master/-/_pages/about.md&quot;,&quot;edit_url&quot;:&quot;/hashemi/AliHashemi-github-io/-/edit/master/_pages/about.md&quot;,&quot;pipeline_editor_url&quot;:&quot;/hashemi/AliHashemi-github-io/-/ci/editor?branch_name=master&quot;,&quot;gitpod_url&quot;:&quot;&quot;,&quot;user_preferences_gitpod_path&quot;:&quot;/-/profile/preferences#user_gitpod_enabled&quot;,&quot;user_profile_enable_gitpod_path&quot;:&quot;/-/user_settings/profile?user%5Bgitpod_enabled%5D=true&quot;,&quot;project_id&quot;:23753,&quot;new_workspace_path&quot;:&quot;/-/remote_development/workspaces/new&quot;,&quot;organization_id&quot;:1,&quot;fork_path&quot;:&quot;/hashemi/AliHashemi-github-io/-/forks/new&quot;,&quot;fork_modal_id&quot;:null}" data-xcode-url="" id="js-repository-blob-header-app"></div>
<div class="info-well">
<div data-history-link="/hashemi/AliHashemi-github-io/-/commits/master" id="js-last-commit"></div>
<div class="gl-hidden @sm/panel:gl-block">

</div>
</div>
<div class="blob-content-holder js-per-page" data-blame-per-page="1000" id="blob-content-holder">
<div data-blob-path="_pages/about.md" data-can-download-code="true" data-escaped-ref="master" data-explain-code-available="false" data-full-name="Ali Hashemi / AliHashemi-github-io" data-has-revs-file="false" data-new-workspace-path="/-/remote_development/workspaces/new" data-organization-id="1" data-original-branch="master" data-project-path="hashemi/AliHashemi-github-io" data-ref-type="heads" data-resource-id="gid://gitlab/Project/23753" data-user-id="" id="js-view-blob-app">
<div class="gl-spinner-container" role="status"><span aria-hidden class="gl-spinner gl-spinner-md gl-spinner-dark !gl-align-text-bottom"></span><span class="gl-sr-only !gl-absolute">Loading</span>
</div>
</div>
</div>

</div>
</div>
<script>
//<![CDATA[
  window.gl = window.gl || {};
  window.gl.webIDEPath = '/-/ide/project/hashemi/AliHashemi-github-io/edit/master/-/_pages/about.md'


//]]>
</script>
<div data-ambiguous="false" data-ref="master" id="js-ambiguous-ref-modal"></div>

</main>
</div>

</div>

</div>
</div>
<div class="js-dynamic-panel paneled-view contextual-panel gl-@container/panel !gl-absolute gl-shadow-lg @xl/content-panels:gl-w-1/2 @xl/content-panels:gl-shadow-none @xl/content-panels:!gl-relative" id="contextual-panel-portal"></div>
</div>
</div>

</div>


<script>
//<![CDATA[
if ('loading' in HTMLImageElement.prototype) {
  document.querySelectorAll('img.lazy').forEach(img => {
    img.loading = 'lazy';
    let imgUrl = img.dataset.src;
    // Only adding width + height for avatars for now
    if (imgUrl.indexOf('/avatar/') > -1 && imgUrl.indexOf('?') === -1) {
      const targetWidth = img.getAttribute('width') || img.width;
      imgUrl += `?width=${targetWidth}`;
    }
    img.src = imgUrl;
    img.removeAttribute('data-src');
    img.classList.remove('lazy');
    img.classList.add('js-lazy-loaded');
    img.dataset.testid = 'js-lazy-loaded-content';
  });
}

//]]>
</script>
<script>
//<![CDATA[
gl = window.gl || {};
gl.experiments = {};


//]]>
</script>

</body>
</html>

