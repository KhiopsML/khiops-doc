/* Kept for CRISP phase content model; this home is now English-only. */
let LANG = 'en';
const I18N = {
  fr:{
    'nav.install':'Installer','nav.install2':'Installation','nav.tutorials':'Tutoriels','nav.api':'API','nav.foundations':'Fondements',
    'hero.lineage1':'25 ans de Recherche Orange','hero.lineage2':'Production industrielle',
    'hero.h1':'ML sur données<br>structurées,<br><em>sans les frictions.</em>',
    'hero.sub':'Pas de feature engineering. Pas d\'hyperparamètres. Pas d\'overfitting. Le formalisme <strong>MODL</strong> gère le pipeline de A à Z — vous vous concentrez sur le problème métier.',
    'hero.id1t':'Issu de la Recherche','hero.id1d':'R&D Orange depuis 1999. Fondements publiés, pair-reviewed, reproductibles.',
    'hero.id2t':'Prêt pour la production','hero.id2d':'Déployé industriellement chez Orange. Out-of-core, distribué, adaptatif.',
    'pill.tabular':'Tabular','pill.multi':'Multi-table','pill.cpp':'C++ optimisé','pill.oss':'Open source',
    'cta.install':'Installer Khiops','cta.demo':'Voir la démo',
    'trust.t1':'Zéro hyperparamètre','trust.t2':'C++ certifié','trust.t3':'Interprétable',
    'code.c1':'# sklearn API — aucune préparation','code.c2':'# multi-table, données brutes OK',
    'stat.hp':'Hyperparamètres','stat.fast':'Plus rapide','stat.interp':'Interprétable',
    'bench.title':'AUC — multi-tables (illustratif)','bench.automl':'AutoML générique',
    'cue.discover':'Découvrir la méthode',
    'crisp.title':'Khiops à chaque étape<br><em>de votre démarche.</em>',
    'crisp.sub':'Un compagnon de méthode qui <strong>compresse radicalement le temps technique</strong> — pour que vous puissiez investir là où ça compte vraiment : comprendre le métier.<br>Survolez chaque phase du cercle.',
    'crisp.idlet':'Six phases.<br>Un compagnon<br>à chaque étape.','crisp.idleh':'Survolez une phase du cercle.',
    'path.beg.t':'Je débute en ML','path.beg.d':'Premier modèle en 30 minutes, sans configuration ni préparation des données.','path.beg.l':'Démarrer le tutoriel',
    'path.ds.t':'Je suis Data Scientist','path.ds.d':'Formalisme MODL, encodages optimaux et performances sur données relationnelles.','path.ds.l':'Explorer les fondements',
    'new.b':'Nouveau','new.t':'Khiops V11 — Shapley, features texte & sparse data',
    'v11.eye':'Nouveautés','v11.title':'La nouvelle version<br><em>repousse les limites.</em>',
    'v11.sub':'Trois avancées majeures dans Khiops V11 — disponibles dès maintenant.',
    'v11.c1t':'Interprétabilité renforcée','v11.c1d':'Khiops calcule <strong>analytiquement les valeurs de Shapley</strong> : contributions exactes par prédiction, sans approximation d\'échantillonnage coûteuse.','v11.c1g':'Shapley natif',
    'v11.c2t':'Le texte devient une feature','v11.c2d':'Les variables textuelles entrent dans la génération automatique de features. <strong>Modélisez directement sur des verbatims</strong> — sans pipeline NLP préalable.','v11.c2g':'Unique sur le marché',
    'v11.c3t':'Volumétries repoussées','v11.c3d':'Implémentation <strong>sparse native</strong> : les données creuses sont traitées sans densification — encore plus de volume accepté en entrée.','v11.c3g':'Sparse data','v11.notes':'Lire les notes de version',
    'dive.hint':'Sous la surface'
  },
  en:{
    'nav.install':'Install','nav.install2':'Install','nav.tutorials':'Tutorials','nav.api':'API','nav.foundations':'Foundations',
    'hero.lineage1':'Open source software','hero.lineage2':'Industrial production',
    'hero.h1':'Built for the hard part<br>of structured-data ML.',
    'hero.sub':'Khiops handles multi-table complexity, large-scale data and manual data preparation work so data scientists can focus on analysis, interpretation and decisions.',
    'hero.id1t':'Research-backed','hero.id1d':'25 years of peer-reviewed research translated into industrial ML execution.',
    'hero.id2t':'Industrial-grade execution','hero.id2d':'Out-of-core, distributed and adaptive execution on industrial-scale data volumes.',
    'pill.tabular':'Tabular','pill.multi':'Multi-table native','pill.cpp':'Out-of-core + distributed','pill.oss':'BSD-3-Clause-Clear',
    'cta.install':'Install Khiops','cta.demo':'Watch the demo',
    'trust.t1':'No tuning loops','trust.t2':'Native multi-table prep','trust.t3':'Interpretable by design',
    'code.c1':'# sklearn API — no manual data preparation','code.c2':'# native multi-table data accepted',
    'stat.hp':'Tuning loops','stat.fast':'Multi-table','stat.interp':'Interpretable',
    'bench.title':'Multi-table benchmark: raw industrial data to model','bench.automl':'Generic AutoML',
    'cue.discover':'Discover the method',
    'crisp.title':'The technical work,<br><em>handled across the lifecycle.</em>',
    'crisp.sub':'Across CRISP-DM, Khiops absorbs repetitive preparation, encoding, modeling and scaling work so teams can invest where expertise matters most: business understanding.',
    'crisp.idlet':'Six phases.<br>One technical backbone<br>for structured data.','crisp.idleh':'Hover over a phase of the wheel.',
    'path.beg.t':'I\'m new to ML','path.beg.d':'Your first model in 30 minutes, with no setup and no data preparation.','path.beg.l':'Start the tutorial',
    'path.ds.t':'I\'m a Data Scientist','path.ds.d':'MODL formalism, optimal encodings and performance on relational data.','path.ds.l':'Explore the foundations',
    'new.b':'New','new.t':'Khiops V11 — Shapley, text features & sparse data',
    'v11.eye':'What\'s new','v11.title':'The new release<br><em>pushes the limits.</em>',
    'v11.sub':'Three major advances in Khiops V11 — available now.',
    'v11.c1t':'Reinforced interpretability','v11.c1d':'Khiops computes <strong>analytical Shapley values</strong>: exact per-prediction contributions, without costly sampling-based approximations.','v11.c1g':'Native Shapley',
    'v11.c2t':'Text becomes a feature','v11.c2d':'Text variables now join automatic feature generation. <strong>Model directly on verbatims</strong> — no upstream NLP pipeline.','v11.c2g':'Unique in the market',
    'v11.c3t':'Volumes pushed further','v11.c3d':'Native <strong>sparse implementation</strong>: sparse data is processed without densification — even larger inputs accepted.','v11.c3g':'Sparse data','v11.notes':'Read the release notes',
    'dive.hint':'Beneath surface'
  }
};

/* SVG wheel phase-name translations (the bold name line in each label) */
const WHEEL_NAMES = {
  fr:['Understanding','Understanding','Preparation','Modeling','Evaluation','Deployment'],
  en:['Understanding','Understanding','Preparation','Modeling','Evaluation','Deployment']
};

function setLang(lang){
  LANG = lang;
  document.documentElement.lang = lang;
  const btnFR = document.getElementById('btnFR');
  const btnEN = document.getElementById('btnEN');
  if (btnFR) btnFR.classList.toggle('on', lang==='fr');
  if (btnEN) btnEN.classList.toggle('on', lang==='en');
  /* text nodes */
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    const k=el.getAttribute('data-i18n'); if(I18N[lang][k]!==undefined) el.textContent=I18N[lang][k];
  });
  document.querySelectorAll('[data-i18n-html]').forEach(el=>{
    const k=el.getAttribute('data-i18n-html'); if(I18N[lang][k]!==undefined) el.innerHTML=I18N[lang][k];
  });
  /* re-render the active phase panel if open */
  if(cur!==-1){ const keep=cur; cur=-1; activate(keep); }
}

const PH=[
  { grad:'G0', lblId:'lbl-0', dot:{x:350,y:77},  lc:'rgba(200,160,32,.9)', tc:'n',
    fr:{ tag:'Phase 01 — Business Understanding',
      ttl:'La seule phase où<br><em>Khiops s\'efface.</em>',
      bdy:'La réflexion métier ne se délègue pas à un algorithme. <strong>Khiops vous redonne du temps pour y exceller</strong> — en automatisant radicalement toutes les phases suivantes.',
      caps:[{i:'ti-clock',c:'n',t:'Investissez ici',b:'Business Understanding est la seule phase que Khiops ne remplace pas. Le temps libéré sur les phases 2 à 6 doit être réinvesti ici — c\'est là que la valeur est créée.'}] },
    en:{ tag:'Phase 01 — Business Understanding',
      ttl:'The phase where<br><em>the objective is defined.</em>',
      bdy:'This phase remains a human responsibility: target definition, decision criteria and operational constraints. <strong>Khiops does not replace this step</strong>; it reduces downstream technical overhead.',
      caps:[{i:'ti-clock',c:'n',t:'Keep expertise here',b:'Use the time saved in phases 2 to 6 to refine hypotheses, costs of errors and deployment constraints.'}] }
  },
  { grad:'G1', lblId:'lbl-1', dot:{x:450,y:250}, lc:'#FF7900', tc:'o',
    fr:{ tag:'Phase 02 — Data Understanding',
      ttl:'Comprendre vos données<br><em>en quelques secondes.</em>',
      bdy:'Avant même de modéliser, Khiops <strong>diagnostique automatiquement</strong> la qualité de vos données et produit des représentations statistiques optimales.',
      caps:[
        {i:'ti-chart-histogram',c:'o',t:'Histogrammes à densité optimale',b:'Discrétisation MODL — chaque bin statistiquement justifié. Distribution, outliers, valeurs manquantes visibles d\'un coup d\'œil.'},
        {i:'ti-shield-check',c:'o',t:'Diagnostic qualité instantané',b:'Variables à faible information, distributions dégénérées — détectées avant toute modélisation.'}] },
    en:{ tag:'Phase 02 — Data Understanding',
      ttl:'Stay focus on <br><em>the story your data tells.</em>',
      bdy:'Khiops processes raw data directly; the time saved on data plumbing allows you to challenge your data—specifically regarding biases, drift, leakage, and so on.',
      caps:[
        {i:'ti-chart-histogram',c:'o',t:'Interpretable summaries',b:'Khiops discretizes categorical and numerical values with MDL complexity control. For example, it finds the optimal number of intervals and their boundaries for each numerical variable.'},
        {i:'ti-shield-check',c:'o',t:'The full information from the raw data',b:'Khiops digests raw data directly, making it possible to preserve the full data signal and leverage all its subtleties.'}] }

  },
  { grad:'G2', lblId:'lbl-2', dot:{x:350,y:423}, lc:'rgba(255,150,48,.9)', tc:'o',
    fr:{ tag:'Phase 03 — Data Preparation',
      ttl:'Préparer les données ?<br><em>Khiops le fait.</em>',
      bdy:'Fini le one-hot encoding, les heuristiques pour valeurs manquantes. <strong>Khiops génère automatiquement les variables pertinentes</strong> pour votre cible.',
      caps:[
        {i:'ti-wand',c:'o',t:'Zéro préparation ad hoc',b:'Pas d\'encodage manuel. Le formalisme MODL traite les données brutes telles qu\'elles arrivent.'},
        {i:'ti-variable',c:'o',t:'Feature engineering automatique',b:'Khiops construit les agrégats pertinents sur données relationnelles — des variables que vous n\'auriez peut-être pas pensé à créer.'}] },
    en:{ tag:'Phase 03 — Data Preparation',
      ttl:'Preparation and encoding<br><em>in one pipeline.</em>',
      bdy:'Encoding and relational aggregates are inferred from the training objective, reducing manual preprocessing scripts and heuristics.',
      caps:[
        {i:'ti-variable',c:'o',t:'Autofeature engineering',b:'Multi-table aggregates are generated and selected in the same workflow. The pipeline is robust, scalable and not prone to overfitting, unlike manual feature engineering.'},
        {i:'ti-function',c:'o',t:'No manual transforms',b:'Log/square transforms and feature normalization are generally unnecessary: rank-based, non-parametric discretization adapts directly to observed values.'}] }
  },
  { grad:'G3', lblId:'lbl-3', dot:{x:150,y:423},  lc:'#3ECFA0', tc:'o',
    fr:{ tag:'Phase 04 — Modeling',
      ttl:'Des modèles précis,<br><em>sans arbitrage.</em>',
      bdy:'Le formalisme MODL garantit des modèles statistiquement optimaux — sans grid search, sans cross-validation coûteuse, sans overfitting par construction.',
      caps:[
        {i:'ti-target',c:'o',t:'Précis & Robuste',b:'Sélection parcimonieuse, encodage optimal intégré — les modèles généralisent bien par nature.'},
        {i:'ti-bolt',c:'g',t:'Automatique & Frugal',b:'Pas d\'hyperparamètre, C++ optimisé. Une fraction du temps et des ressources d\'un AutoML classique.'}],
      extra:'<div class="tagr"><span class="xt o">Précis</span><span class="xt o">Robuste</span><span class="xt g">Automatique</span><span class="xt b">Frugal RAM</span><span class="xt p">Frugal CPU</span></div>' },
    en:{ tag:'Phase 04 — Modeling',
      ttl:'Parsimonious training,<br><em>without tuning loops.</em>',
      bdy:'Training uses a Minimum Description Length (MDL) model-selection criteria from information theory, ensuring statistically optimal models without costly grid search or cross-validation.',
      caps:[
        {i:'ti-bolt',c:'g',t:'Efficient hyperparameter-free formalism',b:'Training is executed once, without cross-validated hyperparameter sweeps.'},
        {i:'ti-target',c:'o',t:'Controlled complexity',b:'Overfitting control is built in: MDL balances model complexity against data fit during training and keeps a small number of features.'},] }
  },
  { grad:'G4', lblId:'lbl-4', dot:{x:50,y:250},  lc:'#29C4C4', tc:'o',
    fr:{ tag:'Phase 05 — Evaluation',
      ttl:'Des modèles que vous pouvez<br><em>expliquer au métier.</em>',
      bdy:'Khiops ne produit pas des boîtes noires. Chaque modèle est <strong>interprétable par construction</strong> — variables, encodages et contributions directement lisibles.',
      caps:[
        {i:'ti-eye',c:'o',t:'Interprétabilité native',b:'Encodages optimaux, contributions par variable — sans post-hoc explainability.'},
        {i:'ti-presentation',c:'o',t:'Présentable au métier',b:'Résultats structurés pour des décideurs non-techniques, sans jargon.'}] },
    en:{ tag:'Phase 05 — Evaluation',
      ttl:'Evaluation with<br><em>auditable outputs.</em>',
      bdy:'Models remain interpretable through explicit encodings, selected variables and additive contributions.',
      caps:[
        {i:'ti-eye',c:'o',t:'Robust by design',b:'The robustness of the formalism allows for confident deployment to production. And if there is no relevant information, the model does not invent anything. Something surprising? Challenge the data, not the model.'},
        {i:'ti-presentation',c:'o',t:'Dedicated visualization tool',b:'The library has an interactive visualization tool that enables access to comprehensive preparation and modelization results directly.'}] }
  },
  { grad:'G5', lblId:'lbl-5', dot:{x:150,y:77},   lc:'#9080FF', tc:'o',
    fr:{ tag:'Phase 06 — Deployment',
      ttl:'Du batch à l\'online,<br><span class="eg">à n\'importe quelle échelle.</span>',
      bdy:'Khiops est conçu pour la production industrielle. <strong>Batch ou temps réel</strong>, sur des volumétries massives avec une empreinte mémoire et CPU maîtrisée, y compris sur des données stockées dans le cloud.',
      caps:[
        {i:'ti-database',c:'o',t:'Volumétries industrielles',b:'Out-of-core nativement — datasets dépassant la RAM, adaptatif au hardware.'},
        {i:'ti-refresh',c:'g',t:'Batch & scoring en ligne (KNI)',b:'Khiops Native Interface permet le scoring temps réel à latence maîtrisée.'},
        {i:'ti-cloud',c:'g',t:'Données cloud',b:'Compatible avec des pipelines sur stockages cloud via connecteurs natifs (GCS/S3) et flux batch industrialisés.'}] },
    en:{ tag:'Phase 06 — Deployment',
      ttl:'Deployment from batch<br><span class="eg">to online scoring.</span>',
      bdy:'The same modeling pipeline can be used in production with controlled resource usage, for both periodic batch runs and low-latency scoring.',
      caps:[
        {i:'ti-database',c:'o',t:'Large-scale execution',b:'Out-of-core and distributed modes support datasets that exceed RAM capacity.'},
        {i:'ti-refresh',c:'g',t:'Batch and KNI scoring',b:'Khiops Native Interface provides predictable latency for real-time integration.'},
        {i:'ti-cloud',c:'g',t:'Cloud-compatible data flows',b:'Operational pipelines can use cloud object storage through native connectors (GCS/S3/Azure).'}] }
  }
];

