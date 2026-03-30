




<!DOCTYPE html>
<html class="gl-system ui-neutral with-top-bar with-header application-chrome page-with-panels with-gl-container-queries  user-logged-out" lang="en">
<head prefix="og: http://ogp.me/ns#">
<meta charset="utf-8">
<meta content="IE=edge" http-equiv="X-UA-Compatible">
<meta content="width=device-width, initial-scale=1" name="viewport">
<title>docs/README.md · v4.199.1 · GitLab.com / Runbooks · GitLab</title>
<script nonce="S4tLmNhxlM65kgiNGBDrUA==">
//<![CDATA[
window.gon={};gon.math_rendering_limits_enabled=true;gon.features={"allowIframesInMarkdown":false,"inlineBlame":false,"repositoryFileTreeBrowser":true,"blobEditRefactor":true,"repositoryLockInformation":false,"convertToGlCiFlowRegistry":true};gon.licensed_features={"fileLocks":true,"remoteDevelopment":true};
//]]>
</script>

<script nonce="S4tLmNhxlM65kgiNGBDrUA==">
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
<script nonce="S4tLmNhxlM65kgiNGBDrUA==">
//<![CDATA[
var gl = window.gl || {};
gl.startup_calls = {"/gitlab-com/runbooks/-/blob/v4.199.1/docs/README.md?format=json\u0026viewer=rich":{}};
gl.startup_graphql_calls = [{"query":"# @feature_category: source_code_management\nquery getBlobInfo(\n  $projectPath: ID!\n  $filePath: [String!]!\n  $ref: String!\n  $refType: RefType\n  $shouldFetchRawText: Boolean!\n) {\n  project(fullPath: $projectPath) {\n    __typename\n    id\n    repository {\n      __typename\n      empty\n      blobs(paths: $filePath, ref: $ref, refType: $refType) {\n        __typename\n        nodes {\n          __typename\n          id\n          webPath\n          name\n          size\n          rawSize\n          rawTextBlob @include(if: $shouldFetchRawText)\n          fileType\n          language\n          path\n          blamePath\n          editBlobPath\n          gitpodBlobUrl\n          ideEditPath\n          forkAndEditPath\n          ideForkAndEditPath\n          codeNavigationPath\n          projectBlobPathRoot\n          forkAndViewPath\n          environmentFormattedExternalUrl\n          environmentExternalUrlForRouteMap\n          canModifyBlob\n          canModifyBlobWithWebIde\n          canCurrentUserPushToBranch\n          archived\n          storedExternally\n          externalStorage\n          externalStorageUrl\n          rawPath\n          replacePath\n          pipelineEditorPath\n          simpleViewer {\n            fileType\n            tooLarge\n            type\n            renderError\n          }\n          richViewer {\n            fileType\n            tooLarge\n            type\n            renderError\n          }\n        }\n      }\n    }\n  }\n}\n","variables":{"projectPath":"gitlab-com/runbooks","ref":"v4.199.1","refType":"TAGS","filePath":"docs/README.md","shouldFetchRawText":false}}];

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
  const headers = {"X-CSRF-Token":"Xn0_o9nI_sGr2ULBwor1DD_GwcyBKveTUdCMpsxwcdK8TSYiIHYNeHyuob3tOcr572EMgt5vgPHFjyG5DlGahw","x-gitlab-feature-category":"source_code_management"};
  const url = `https://gitlab.com/api/graphql`

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
<link rel="stylesheet" href="/assets/application-ec62ea55bf9350451bbd314236d53a671514ec727250c238949651333a593457.css" media="(prefers-color-scheme: light)" />
<link rel="stylesheet" href="/assets/application_dark-f0efcc87575ba79fe9743ec9b1c7830bbc7d778bf69f278e2f726ef959d0252b.css" media="(prefers-color-scheme: dark)" />
<link rel="stylesheet" href="/assets/page_bundles/tree-fb7df91c595e3158c2ad5a485cfb0039d488d3ba8e39d62b61cd585c78608e64.css" /><link rel="stylesheet" href="/assets/page_bundles/projects-1e46068245452053a00290f44a0ebda348b43ba90e413a07b9d36767e72b79aa.css" /><link rel="stylesheet" href="/assets/page_bundles/commit_description-9e7efe20f0cef17d0606edabfad0418e9eb224aaeaa2dae32c817060fa60abcc.css" /><link rel="stylesheet" href="/assets/page_bundles/work_items-af321897c3b1ae7c1f6f0cb993681211b837df7ec8e5ff59e3795fd08ab83a13.css" /><link rel="stylesheet" href="/assets/page_bundles/notes_shared-e58f07f39b2c4557134baf9f32b68c875fffb37fe1c5d8808fb7607d19f5690b.css" />
<link rel="stylesheet" href="/assets/tailwind_cqs-e4779258317efe2bae0b955f419bd7c2616663afbdf5f31579ff8058de54732b.css" />


<link rel="stylesheet" href="/assets/fonts-deb7ad1d55ca77c0172d8538d53442af63604ff490c74acc2859db295c125bdb.css" />
<link rel="stylesheet" href="/assets/highlight/themes/white-d436882f650831f756a6394bdaa66486d5ef99218601d4839f4d640558a4f307.css" media="(prefers-color-scheme: light)" />
<link rel="stylesheet" href="/assets/highlight/themes/dark-9afe7e06099105c59ea8fe5379843ddf5c5dfcb3cc523eed3a9d4147f6ba7c5b.css" media="(prefers-color-scheme: dark)" />

<script src="/assets/webpack/runtime.6e112eee.bundle.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/main.9ee5ca99.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/tracker.1eb446cb.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script nonce="S4tLmNhxlM65kgiNGBDrUA==">
//<![CDATA[
window.snowplowOptions = {"namespace":"gl","hostname":"snowplowprd.trx.gitlab.net","cookieDomain":".gitlab.com","appId":"gitlab","formTracking":true,"linkClickTracking":true};
gl = window.gl || {};
gl.snowplowStandardContext = {"schema":"iglu:com.gitlab/gitlab_standard/jsonschema/1-1-7","data":{"environment":"production","source":"gitlab-rails","correlation_id":"9e3db8bdad05f7bb-LAX","extra":{},"user_id":null,"global_user_id":null,"user_type":null,"is_gitlab_team_member":null,"namespace_id":6543,"ultimate_parent_namespace_id":6543,"project_id":1148549,"feature_enabled_by_namespace_ids":null,"realm":"saas","deployment_type":".com","context_generated_at":"2026-03-29T09:06:59.159Z"}};
gl.snowplowPseudonymizedPageUrl = "https://gitlab.com/namespace6543/project1148549/-/blob/:repository_path";
gl.maskedDefaultReferrerUrl = null;
gl.ga4MeasurementId = 'G-ENFH3X7M5Y';
gl.duoEvents = ["ai_question_category","perform_completion_worker","process_gitlab_duo_question","agent_platform_session_created","agent_platform_session_dropped","agent_platform_session_finished","agent_platform_session_resumed","agent_platform_session_started","agent_platform_session_stopped","ai_response_time","ci_repository_xray_artifact_created","cleanup_stuck_agent_platform_session","click_dap_trial_or_paid_empty_state_agent","click_dap_trial_or_paid_empty_state_explore_agents_link","click_dap_trial_or_paid_empty_state_prompt","click_delete_ai_catalog_item_button","click_disable_ai_catalog_item_button","click_duo_agentic_not_available_empty_state_learn_more","click_duo_agentic_not_available_empty_state_start_trial","click_duo_agentic_trial_expired_learn_more","click_duo_agentic_trial_expired_upgrade","click_duplicate_ai_catalog_item_button","click_enable_ai_catalog_item_button","click_purchase_seats_button_group_duo_pro_home_page","close_vulnerability_resolution_merge_request","code_suggestion_accepted_in_ide","code_suggestion_rejected_in_ide","code_suggestion_shown_in_ide","code_suggestions_connection_details_rate_limit_exceeded","code_suggestions_direct_access_rate_limit_exceeded","code_suggestions_rate_limit_exceeded","create_ai_catalog_item","create_ai_catalog_item_consumer","create_ai_self_hosted_model","create_vulnerability_resolution_merge_request","default_answer","delete_ai_catalog_item","delete_ai_catalog_item_consumer","delete_ai_self_hosted_model","detected_high_comment_temperature","detected_repeated_high_comment_temperature","dismiss_sast_vulnerability_false_positive_analysis","dismiss_secret_detection_vulnerability_false_positive_analysis","encounter_duo_code_review_error_during_review","error_answer","excluded_files_from_duo_code_review","execute_llm_method","filter_ai_fp","find_no_issues_duo_code_review_after_review","find_nothing_to_review_duo_code_review_on_mr","finish_duo_workflow_execution","finish_mcp_tool_call","forced_high_temperature_commenting","i_quickactions_q","include_repository_xray_data_into_code_generation_prompt","mention_gitlabduo_in_mr_comment","merge_vulnerability_resolution_merge_request","post_comment_duo_code_review_on_diff","process_gitlab_duo_slash_command","react_thumbs_down_on_duo_code_review_comment","react_thumbs_up_on_duo_code_review_comment","reported_sast_vulnerability_false_positive_analysis","reported_secret_detection_vulnerability_false_positive_analysis","request_ask_help","request_duo_chat_response","request_review_duo_code_review_on_mr_by_author","request_review_duo_code_review_on_mr_by_non_author","requested_comment_temperature","retry_duo_workflow_execution","start_duo_workflow_execution","start_mcp_tool_call","submit_dap_trial_or_paid_empty_state_message","submit_gitlab_duo_question","tokens_per_embedding","tokens_per_user_request_prompt","tokens_per_user_request_response","trigger_ai_catalog_item","trigger_sast_vulnerability_fp_detection_workflow","trigger_sast_vulnerability_resolution_workflow","trigger_secret_detection_vulnerability_fp_detection_workflow","troubleshoot_job","update_ai_catalog_item","update_ai_catalog_item_consumer","update_ai_self_hosted_model","update_model_selection_feature","update_self_hosted_ai_feature_to_vendored_model","view_ai_catalog_item","view_ai_catalog_item_index","view_ai_catalog_project_catalog","view_ai_catalog_project_managed","view_dap_trial_or_paid_empty_state","view_duo_agentic_not_available_empty_state","view_duo_agentic_trial_expired_empty_state"];
gl.onlySendDuoEvents = false;


//]]>
</script>
<link rel="preload" href="/assets/application-ec62ea55bf9350451bbd314236d53a671514ec727250c238949651333a593457.css" as="style" type="text/css" nonce="yUKg3ssY6F1lAwlyJo8kPg==">
<link rel="preload" href="/assets/highlight/themes/white-d436882f650831f756a6394bdaa66486d5ef99218601d4839f4d640558a4f307.css" as="style" type="text/css" nonce="yUKg3ssY6F1lAwlyJo8kPg==">
<link crossorigin="" href="https://snowplowprd.trx.gitlab.net" rel="preconnect">
<link as="font" crossorigin="" href="/assets/gitlab-sans/GitLabSans-9892dc17af892e03de41625c0ee325117a3b8ee4ba6005f3a3eac68510030aed.woff2" rel="preload">
<link as="font" crossorigin="" href="/assets/gitlab-sans/GitLabSans-Italic-f96f17332d67b21ada2dfba5f0c0e1d5801eab99330472057bf18edd93d4ccf7.woff2" rel="preload">
<link as="font" crossorigin="" href="/assets/gitlab-mono/GitLabMono-29c2152dac8739499dd0fe5cd37a486ebcc7d4798c9b6d3aeab65b3172375b05.woff2" rel="preload">
<link as="font" crossorigin="" href="/assets/gitlab-mono/GitLabMono-Italic-af36701a2188df32a9dcea12e0424c380019698d4f76da9ad8ea2fd59432cf83.woff2" rel="preload">
<link rel="preload" href="/assets/fonts-deb7ad1d55ca77c0172d8538d53442af63604ff490c74acc2859db295c125bdb.css" as="style" type="text/css" nonce="yUKg3ssY6F1lAwlyJo8kPg==">



<script src="/assets/webpack/sentry.914a2c3f.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>

<script src="/assets/webpack/super_sidebar.8b5d9315.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/commons-pages.groups-pages.groups.achievements-pages.groups.activity-pages.groups.analytics.ci_cd_an-6c07bffb.5b2b94e1.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/commons-pages.groups.epics.index-pages.groups.epics.new-pages.groups.epics.show-pages.groups.issues--a711c0bb.87612578.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/ea7ea8c3.35bd07e7.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/commons-pages.projects.blob.edit-pages.projects.blob.new-pages.projects.blob.show-pages.projects.get-487ddc08.c5a96f47.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/3808d5a6.b2f16697.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.show-pages.projects.snippets.show-pages.projects.tre-c684fcf6.7dfd64bd.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/35610df2.587c0bbd.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.commits.show-pages.projects.show-pages.projects.tree.show.664d637b.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/commons-pages.projects.blame.show-pages.projects.blob.show-pages.projects.show-pages.projects.tree.show.739ab2e2.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/commons-pages.groups.show-pages.projects.blob.show-pages.projects.show-pages.projects.tree.show.3c4762f9.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.show-pages.projects.tree.show.e8cb81ee.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.tree.show-treeList.b5051ff8.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>
<script src="/assets/webpack/pages.projects.blob.show.43555750.chunk.js" defer="defer" nonce="S4tLmNhxlM65kgiNGBDrUA=="></script>

<meta content="object" property="og:type">
<meta content="GitLab" property="og:site_name">
<meta content="docs/README.md · v4.199.1 · GitLab.com / Runbooks · GitLab" property="og:title">
<meta content="Runbooks for the stressed on-call https://runbooks.gitlab.com Mirrored to https://ops.gitlab.net/gitlab-com/runbooks" property="og:description">
<meta content="https://gitlab.com/uploads/-/system/project/avatar/1148549/dont_panic_towel.jpg" property="og:image">
<meta content="64" property="og:image:width">
<meta content="64" property="og:image:height">
<meta content="https://gitlab.com/gitlab-com/runbooks/-/blob/v4.199.1/docs/README.md" property="og:url">
<meta content="summary" property="twitter:card">
<meta content="docs/README.md · v4.199.1 · GitLab.com / Runbooks · GitLab" property="twitter:title">
<meta content="Runbooks for the stressed on-call https://runbooks.gitlab.com Mirrored to https://ops.gitlab.net/gitlab-com/runbooks" property="twitter:description">
<meta content="https://gitlab.com/uploads/-/system/project/avatar/1148549/dont_panic_towel.jpg" property="twitter:image">

<meta name="csrf-param" content="authenticity_token" />
<meta name="csrf-token" content="2u2qKDRHD5BFWgDRrFwbLXXhH8OAjYdgEG-ny0k_Hsg43bOpzfn8KZIt462D7yTYpUbSjd_I8AKEMArUix71nQ" />
<meta name="csp-nonce" content="S4tLmNhxlM65kgiNGBDrUA==" />
<meta name="action-cable-url" content="/-/cable" />
<link href="/-/manifest.json" rel="manifest">
<link rel="icon" type="image/png" href="/assets/favicon-yellow-018213ceb87b472388095d0264be5b4319ef47471dacea03c83ecc233ced2fd5.png" id="favicon" data-original-href="/assets/favicon-yellow-018213ceb87b472388095d0264be5b4319ef47471dacea03c83ecc233ced2fd5.png" />
<link rel="apple-touch-icon" type="image/x-icon" href="/assets/apple-touch-icon-b049d4bc0dd9626f31db825d61880737befc7835982586d015bded10b4435460.png" />
<link href="/search/opensearch.xml" rel="search" title="Search GitLab" type="application/opensearchdescription+xml">




<meta content="Runbooks for the stressed on-call https://runbooks.gitlab.com Mirrored to https://ops.gitlab.net/gitlab-com/runbooks" name="description">
<meta content="#F1F0F6" media="(prefers-color-scheme: light)" name="theme-color">
<meta content="#232128" media="(prefers-color-scheme: dark)" name="theme-color">
</head>

<body class="tab-width-8 gl-browser-generic gl-platform-other" data-group="gitlab-com" data-group-full-path="gitlab-com" data-namespace-id="6543" data-page="projects:blob:show" data-page-type-id="v4.199.1/docs/README.md" data-project="runbooks" data-project-full-path="gitlab-com/runbooks" data-project-id="1148549">
<div id="js-tooltips-container"></div>

<script nonce="S4tLmNhxlM65kgiNGBDrUA==">
//<![CDATA[
gl = window.gl || {};
gl.client = {"isGeneric":true,"isOther":true};


//]]>
</script>


<header class="super-topbar js-super-topbar"></header>
<div class="layout-page js-page-layout page-with-super-sidebar">
<script nonce="S4tLmNhxlM65kgiNGBDrUA==">
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
</script><aside class="js-super-sidebar super-sidebar super-sidebar-loading" data-command-palette="{&quot;project_files_url&quot;:&quot;/gitlab-com/runbooks/-/files/v4.199.1?format=json&quot;,&quot;project_blob_url&quot;:&quot;/gitlab-com/runbooks/-/blob/v4.199.1&quot;}" data-is-saas="true" data-root-path="/" data-sidebar="{&quot;whats_new_most_recent_release_items_count&quot;:5,&quot;whats_new_version_digest&quot;:&quot;b4bb533fa95c6f945110887a7a55cb5876d00a039246e10eeb15e8f878438cd2&quot;,&quot;whats_new_read_articles&quot;:[],&quot;whats_new_mark_as_read_path&quot;:&quot;/-/whats_new/mark_as_read&quot;,&quot;is_logged_in&quot;:false,&quot;compare_plans_url&quot;:&quot;https://about.gitlab.com/pricing&quot;,&quot;context_switcher_links&quot;:[{&quot;title&quot;:&quot;Explore&quot;,&quot;link&quot;:&quot;/explore&quot;,&quot;icon&quot;:&quot;compass&quot;}],&quot;current_menu_items&quot;:[{&quot;id&quot;:&quot;project_overview&quot;,&quot;title&quot;:&quot;Runbooks&quot;,&quot;avatar&quot;:&quot;/uploads/-/system/project/avatar/1148549/dont_panic_towel.jpg&quot;,&quot;entity_id&quot;:1148549,&quot;link&quot;:&quot;/gitlab-com/runbooks&quot;,&quot;link_classes&quot;:&quot;shortcuts-project&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;manage_menu&quot;,&quot;title&quot;:&quot;Manage&quot;,&quot;icon&quot;:&quot;users&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/activity&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;activity&quot;,&quot;title&quot;:&quot;Activity&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/activity&quot;,&quot;link_classes&quot;:&quot;shortcuts-project-activity&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;members&quot;,&quot;title&quot;:&quot;Members&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/project_members&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;labels&quot;,&quot;title&quot;:&quot;Labels&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/labels&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;plan_menu&quot;,&quot;title&quot;:&quot;Plan&quot;,&quot;icon&quot;:&quot;planning&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/work_items&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;project_issue_list&quot;,&quot;title&quot;:&quot;Work items&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/work_items&quot;,&quot;link_classes&quot;:&quot;shortcuts-issues has-sub-items&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;boards&quot;,&quot;title&quot;:&quot;Issue boards&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/boards&quot;,&quot;link_classes&quot;:&quot;shortcuts-issue-boards&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;milestones&quot;,&quot;title&quot;:&quot;Milestones&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/milestones&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;iterations&quot;,&quot;title&quot;:&quot;Iterations&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/cadences&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;requirements&quot;,&quot;title&quot;:&quot;Requirements&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/requirements_management/requirements&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;external_issue_tracker&quot;,&quot;title&quot;:&quot;Custom issue tracker&quot;,&quot;link&quot;:&quot;https://gitlab.com/gitlab-com/gl-infra/infrastructure&quot;,&quot;link_classes&quot;:&quot;shortcuts-external_tracker&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;code_menu&quot;,&quot;title&quot;:&quot;Code&quot;,&quot;icon&quot;:&quot;code&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/merge_requests&quot;,&quot;is_active&quot;:true,&quot;items&quot;:[{&quot;id&quot;:&quot;project_merge_request_list&quot;,&quot;title&quot;:&quot;Merge requests&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/merge_requests&quot;,&quot;link_classes&quot;:&quot;shortcuts-merge_requests&quot;,&quot;pill_count_field&quot;:&quot;openMergeRequestsCount&quot;,&quot;pill_count_dynamic&quot;:false,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;files&quot;,&quot;title&quot;:&quot;Repository&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/tree/v4.199.1&quot;,&quot;link_classes&quot;:&quot;shortcuts-tree&quot;,&quot;is_active&quot;:true},{&quot;id&quot;:&quot;branches&quot;,&quot;title&quot;:&quot;Branches&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/branches&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;commits&quot;,&quot;title&quot;:&quot;Commits&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/commits/v4.199.1?ref_type=tags&quot;,&quot;link_classes&quot;:&quot;shortcuts-commits&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;tags&quot;,&quot;title&quot;:&quot;Tags&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/tags&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;graphs&quot;,&quot;title&quot;:&quot;Repository graph&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/network/v4.199.1?ref_type=tags&quot;,&quot;link_classes&quot;:&quot;shortcuts-network&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;compare&quot;,&quot;title&quot;:&quot;Compare revisions&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/compare?from=master\u0026to=v4.199.1&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;project_snippets&quot;,&quot;title&quot;:&quot;Snippets&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/snippets&quot;,&quot;link_classes&quot;:&quot;shortcuts-snippets&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;file_locks&quot;,&quot;title&quot;:&quot;Locked files&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/path_locks&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;deploy_menu&quot;,&quot;title&quot;:&quot;Deploy&quot;,&quot;icon&quot;:&quot;deployments&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/releases&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;releases&quot;,&quot;title&quot;:&quot;Releases&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/releases&quot;,&quot;link_classes&quot;:&quot;shortcuts-deployments-releases&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;container_registry&quot;,&quot;title&quot;:&quot;Container registry&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/container_registry&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;model_registry&quot;,&quot;title&quot;:&quot;Model registry&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/ml/models&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;operations_menu&quot;,&quot;title&quot;:&quot;Operate&quot;,&quot;icon&quot;:&quot;cloud-pod&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/environments&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;environments&quot;,&quot;title&quot;:&quot;Environments&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/environments&quot;,&quot;link_classes&quot;:&quot;shortcuts-environments&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;monitor_menu&quot;,&quot;title&quot;:&quot;Monitor&quot;,&quot;icon&quot;:&quot;monitor&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/incidents&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;incidents&quot;,&quot;title&quot;:&quot;Incidents&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/incidents&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;analyze_menu&quot;,&quot;title&quot;:&quot;Analyze&quot;,&quot;icon&quot;:&quot;chart&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/value_stream_analytics&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;cycle_analytics&quot;,&quot;title&quot;:&quot;Value stream analytics&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/value_stream_analytics&quot;,&quot;link_classes&quot;:&quot;shortcuts-project-cycle-analytics&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;contributors&quot;,&quot;title&quot;:&quot;Contributor analytics&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/graphs/v4.199.1?ref_type=tags&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;repository_analytics&quot;,&quot;title&quot;:&quot;Repository analytics&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/graphs/v4.199.1/charts&quot;,&quot;link_classes&quot;:&quot;shortcuts-repository-charts&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;code_review&quot;,&quot;title&quot;:&quot;Code review analytics&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/analytics/code_reviews&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;issues&quot;,&quot;title&quot;:&quot;Issue analytics&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/analytics/issues_analytics&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;insights&quot;,&quot;title&quot;:&quot;Insights&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/insights/&quot;,&quot;link_classes&quot;:&quot;shortcuts-project-insights&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;model_experiments&quot;,&quot;title&quot;:&quot;Model experiments&quot;,&quot;link&quot;:&quot;/gitlab-com/runbooks/-/ml/experiments&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false}],&quot;current_context_header&quot;:&quot;Project&quot;,&quot;university_path&quot;:&quot;https://university.gitlab.com&quot;,&quot;support_path&quot;:&quot;https://support.gitlab.com&quot;,&quot;docs_path&quot;:&quot;/help/docs&quot;,&quot;display_whats_new&quot;:true,&quot;show_version_check&quot;:null,&quot;search&quot;:{&quot;search_path&quot;:&quot;/search&quot;,&quot;issues_path&quot;:&quot;/dashboard/issues&quot;,&quot;mr_path&quot;:&quot;/dashboard/merge_requests&quot;,&quot;autocomplete_path&quot;:&quot;/search/autocomplete&quot;,&quot;settings_path&quot;:&quot;/search/settings&quot;,&quot;search_context&quot;:{&quot;group&quot;:{&quot;id&quot;:6543,&quot;name&quot;:&quot;GitLab.com&quot;,&quot;full_name&quot;:&quot;GitLab.com&quot;},&quot;group_metadata&quot;:{&quot;issues_path&quot;:&quot;/groups/gitlab-com/-/issues&quot;,&quot;mr_path&quot;:&quot;/groups/gitlab-com/-/merge_requests&quot;},&quot;project&quot;:{&quot;id&quot;:1148549,&quot;name&quot;:&quot;Runbooks&quot;},&quot;project_metadata&quot;:{&quot;mr_path&quot;:&quot;/gitlab-com/runbooks/-/merge_requests&quot;,&quot;issues_path&quot;:&quot;/gitlab-com/runbooks/-/issues&quot;},&quot;code_search&quot;:true,&quot;ref&quot;:&quot;v4.199.1&quot;,&quot;scope&quot;:null,&quot;for_snippets&quot;:null}},&quot;panel_type&quot;:&quot;project&quot;,&quot;shortcut_links&quot;:[{&quot;title&quot;:&quot;Snippets&quot;,&quot;href&quot;:&quot;/explore/snippets&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-snippets&quot;},{&quot;title&quot;:&quot;Groups&quot;,&quot;href&quot;:&quot;/explore/groups&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-groups&quot;},{&quot;title&quot;:&quot;Projects&quot;,&quot;href&quot;:&quot;/explore/projects&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-projects&quot;}],&quot;terms&quot;:&quot;/-/users/terms&quot;,&quot;sign_in_visible&quot;:&quot;true&quot;,&quot;allow_signup&quot;:&quot;true&quot;,&quot;new_user_registration_path&quot;:&quot;/users/sign_up&quot;,&quot;sign_in_path&quot;:&quot;/users/sign_in?redirect_to_referer=yes&quot;,&quot;trial_registration_path&quot;:&quot;/-/trial_registrations/new&quot;}"></aside>

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
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"GitLab.com","item":"https://gitlab.com/gitlab-com"},{"@type":"ListItem","position":2,"name":"Runbooks","item":"https://gitlab.com/gitlab-com/runbooks"},{"@type":"ListItem","position":3,"name":"Repository","item":"https://gitlab.com/gitlab-com/runbooks/-/blob/v4.199.1/docs/README.md"}]}


</script>
<div data-testid="breadcrumb-links" id="js-vue-page-breadcrumbs-wrapper">
<div data-breadcrumbs-json="[{&quot;text&quot;:&quot;GitLab.com&quot;,&quot;href&quot;:&quot;/gitlab-com&quot;,&quot;avatarPath&quot;:&quot;/uploads/-/system/group/avatar/6543/gitlab_logo_192x192.png&quot;},{&quot;text&quot;:&quot;Runbooks&quot;,&quot;href&quot;:&quot;/gitlab-com/runbooks&quot;,&quot;avatarPath&quot;:&quot;/uploads/-/system/project/avatar/1148549/dont_panic_towel.jpg&quot;},{&quot;text&quot;:&quot;Repository&quot;,&quot;href&quot;:&quot;/gitlab-com/runbooks/-/blob/v4.199.1/docs/README.md&quot;,&quot;avatarPath&quot;:null}]" id="js-vue-page-breadcrumbs"></div>
<div id="js-injected-page-breadcrumbs"></div>
</div>
<div id="js-page-breadcrumbs-extra"></div>


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








<div class="js-signature-container" data-signatures-path="/gitlab-com/runbooks/-/commits/088b8f343a8e65b11f5b7ad27f6b81f55a66e607/signatures?limit=1"></div>

<div class="gl-flex navigation-root">
<div id="js-file-browser" style="width:320px"></div>
<div class="tree-holder gl-pt-5 gl-pl-4 gl-w-full gl-min-w-0" id="tree-holder">
<div data-blob-path="docs/README.md" data-breadcrumbs-can-collaborate="false" data-breadcrumbs-can-edit-tree="false" data-breadcrumbs-can-push-code="false" data-breadcrumbs-can-push-to-branch="false" data-breadcrumbs-new-blob-path="/gitlab-com/runbooks/-/new/v4.199.1" data-breadcrumbs-new-branch-path="/gitlab-com/runbooks/-/branches/new" data-breadcrumbs-new-dir-path="/gitlab-com/runbooks/-/create_dir/v4.199.1" data-breadcrumbs-new-tag-path="/gitlab-com/runbooks/-/tags/new" data-breadcrumbs-upload-path="/gitlab-com/runbooks/-/create/v4.199.1" data-download-links="[{&quot;text&quot;:&quot;zip&quot;,&quot;path&quot;:&quot;/gitlab-com/runbooks/-/archive/v4.199.1/runbooks-v4.199.1.zip&quot;},{&quot;text&quot;:&quot;tar.gz&quot;,&quot;path&quot;:&quot;/gitlab-com/runbooks/-/archive/v4.199.1/runbooks-v4.199.1.tar.gz&quot;},{&quot;text&quot;:&quot;tar.bz2&quot;,&quot;path&quot;:&quot;/gitlab-com/runbooks/-/archive/v4.199.1/runbooks-v4.199.1.tar.bz2&quot;},{&quot;text&quot;:&quot;tar&quot;,&quot;path&quot;:&quot;/gitlab-com/runbooks/-/archive/v4.199.1/runbooks-v4.199.1.tar&quot;}]" data-escaped-ref="v4.199.1" data-history-link="/gitlab-com/runbooks/-/commits/v4.199.1" data-http-url="https://gitlab.com/gitlab-com/runbooks.git" data-new-workspace-path="/-/remote_development/workspaces/new" data-organization-id="1" data-project-id="1148549" data-project-path="gitlab-com/runbooks" data-project-root-path="/gitlab-com/runbooks" data-project-short-path="runbooks" data-ref="v4.199.1" data-ref-type="tags" data-root-ref="master" data-show-no-ssh-key-message="" data-ssh-url="git@gitlab.com:gitlab-com/runbooks.git" data-user-settings-ssh-keys-path="/-/user_settings/ssh_keys" data-web-ide-button-default-branch="master" data-web-ide-button-options="{&quot;project_path&quot;:&quot;gitlab-com/runbooks&quot;,&quot;ref&quot;:&quot;v4.199.1&quot;,&quot;is_fork&quot;:false,&quot;needs_to_fork&quot;:true,&quot;gitpod_enabled&quot;:false,&quot;is_blob&quot;:true,&quot;show_edit_button&quot;:false,&quot;show_web_ide_button&quot;:false,&quot;show_gitpod_button&quot;:false,&quot;show_pipeline_editor_button&quot;:false,&quot;web_ide_url&quot;:&quot;/-/ide/project/gitlab-com/runbooks/edit/v4.199.1/-/docs/README.md&quot;,&quot;edit_url&quot;:&quot;/gitlab-com/runbooks/-/edit/v4.199.1/docs/README.md&quot;,&quot;pipeline_editor_url&quot;:&quot;/gitlab-com/runbooks/-/ci/editor?branch_name=v4.199.1&quot;,&quot;gitpod_url&quot;:&quot;https://gitpod.io/#https://gitlab.com/gitlab-com/runbooks/-/tree/v4.199.1/docs/README.md&quot;,&quot;user_preferences_gitpod_path&quot;:&quot;/-/profile/preferences#user_gitpod_enabled&quot;,&quot;user_profile_enable_gitpod_path&quot;:&quot;/-/user_settings/profile?user%5Bgitpod_enabled%5D=true&quot;,&quot;project_id&quot;:1148549,&quot;new_workspace_path&quot;:&quot;/-/remote_development/workspaces/new&quot;,&quot;organization_id&quot;:1,&quot;fork_path&quot;:&quot;/gitlab-com/runbooks/-/forks/new&quot;,&quot;fork_modal_id&quot;:null}" data-xcode-url="" id="js-repository-blob-header-app"></div>
<div class="info-well">
<div data-history-link="/gitlab-com/runbooks/-/commits/v4.199.1" id="js-last-commit"></div>
<div class="gl-hidden @sm/panel:gl-block">
<div data-blob-path="docs/README.md" data-branch="v4.199.1" data-branch-rules-path="/gitlab-com/runbooks/-/settings/repository#js-branch-rules" data-project-path="gitlab-com/runbooks" id="js-code-owners"></div>

</div>
</div>
<div class="blob-content-holder js-per-page" data-blame-per-page="1000" id="blob-content-holder">
<div data-blob-path="docs/README.md" data-can-download-code="true" data-escaped-ref="v4.199.1" data-explain-code-available="false" data-full-name="GitLab.com / Runbooks" data-has-revs-file="false" data-new-workspace-path="/-/remote_development/workspaces/new" data-organization-id="1" data-original-branch="v4.199.1" data-project-path="gitlab-com/runbooks" data-ref-type="tags" data-resource-id="gid://gitlab/Project/1148549" data-user-id="" id="js-view-blob-app">
<div class="gl-spinner-container" role="status"><span aria-hidden class="gl-spinner gl-spinner-md gl-spinner-dark !gl-align-text-bottom"></span><span class="gl-sr-only !gl-absolute">Loading</span>
</div>
</div>
</div>

</div>
</div>
<script nonce="S4tLmNhxlM65kgiNGBDrUA==">
//<![CDATA[
  window.gl = window.gl || {};
  window.gl.webIDEPath = '/-/ide/project/gitlab-com/runbooks/edit/v4.199.1/-/docs/README.md'


//]]>
</script>
<div data-ambiguous="false" data-ref="v4.199.1" id="js-ambiguous-ref-modal"></div>

</main>
</div>

</div>

</div>
</div>
<div class="js-dynamic-panel paneled-view contextual-panel gl-@container/panel !gl-absolute gl-shadow-lg @xl/content-panels:gl-w-1/2 @xl/content-panels:gl-shadow-none @xl/content-panels:!gl-relative" id="contextual-panel-portal"></div>
</div>
</div>


</div>


<script nonce="S4tLmNhxlM65kgiNGBDrUA==">
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
<script nonce="S4tLmNhxlM65kgiNGBDrUA==">
//<![CDATA[
gl = window.gl || {};
gl.experiments = {};


//]]>
</script>

</body>
</html>

