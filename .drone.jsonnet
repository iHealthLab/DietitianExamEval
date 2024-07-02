local env = {
  main: {
    clusterName: 'dev-new',
    instance: 'dev-drone.ihealth-eng.com',
  },
  release: {
    clusterName: 'prod',
    instance: 'prod-drone.ihealth-eng.com',
  },
};

local config = function(branchName) {
  DOCKER_USERNAME: {
    from_secret: 'IHEALTH_DOCKER_USERNAME',
  },
  DOCKER_PASSWORD: {
    from_secret: 'IHEALTH_DOCKER_PASSWORD',
  },
  ENVIRONMENT: env[branchName].clusterName,
  TAG: '${DRONE_COMMIT_SHA:0:8}',
  MYSQL_HOST: {
    from_secret: 'MYSQL_HOST',
  },
  MYSQL_USER: {
    from_secret: 'MYSQL_USER',
  },
  MYSQL_PASSWORD: {
    from_secret: 'MYSQL_PASSWORD',
  },
  GEMINI_API_KEY: {
    from_secret: 'GEMINI_API_KEY',
  },
  OPENAI_API_KEY: {
    from_secret: 'OPENAI_API_KEY',
  },
};

local getCondition = function(branchName, event) {
  instance: env[branchName].instance,
  event: event,
};

local build = function(branchName) {
  name: 'Build',
  image: 'python:3.12',
  pull: 'if-not-exists',
  commands: [
    'pip install -r requirements.txt',
  ],
  when: getCondition(branchName, ['push']),
};

local gpt_exp = function(branchName) {
  name: 'GPT Experiment',
  image: 'python:3.12',
  pull: 'if-not-exists',
  commands: [
    'echo $ENV > .env',
    'pip install -r requirements.txt',
    'pwd',
    'ls -al .env',
    'echo $ENV',
    'echo $MYSQL_PORT',
    'echo $DB_NAME',
    'python com/ihealthlabs/common/gpt_exp.py'
  ],
  when: getCondition(branchName, ['push']),
  environment: config(branchName),
};


local publish = function(branchName, name) {
  name: 'Publish_' + name,
  image: 'plugins/docker',
  pull: 'if-not-exists',
  settings: {
    username: {
      from_secret: 'IHEALTH_DOCKER_USERNAME',
    },
    password: {
      from_secret: 'IHEALTH_DOCKER_PASSWORD',
    },
    repo: 'ihealthlab/ai-benchmark-' + name,
    tags: '${DRONE_COMMIT_SHA:0:8}',
    dockerfile: './' + name + '/Dockerfile',
    context: './' + name,
  },
  resources: {
    requests: {
      cpu: 10,
      memory: '250MiB',
    },
    limits: {
      cpu: 1000,
      memory: '4000MiB',
    },
  },
  when: getCondition(branchName, ['push']),
};

local deployCommands = function(name) {
  command: [
    "(echo 'cat <<EOF' ; cat k8s/" + name + '.yml ; echo EOF) | sh > ' + name + '.yml',
    'kubectl -n $NAMESPACE apply -f ' + name + '.yml',
  ],
};

local deploy = function(branchName) {
  name: 'Deploy',
  image: 'ihealthlab/deploy-tools:1.0',
  commands: ['aws eks update-kubeconfig --name $ENVIRONMENT-k8s-cluster --role-arn $AWS_ACCOUNT_ID:role/$ENVIRONMENT-k8s-admin']
            + deployCommands('api').command,
  when: getCondition(branchName, ['push']),
  environment: config(branchName),
};


local cdPipeline = function(branchName) {
  kind: 'pipeline',
  type: 'kubernetes',
  name: branchName + '_cd',
  steps: [
    gpt_exp(branchName),
  ],
  trigger: {
    branch: branchName,
    event: 'push',
  },
  image_pull_secrets: ['IHEALTH_DOCKER_CONFIGURATION_JSON'],
};


[
  cdPipeline('main'),
  cdPipeline('release'),
]
