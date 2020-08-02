
#!/bin/bash
#
# Publish images to your ECR account.

# 기존 소스에서 아래 주석 처리 함
# set -euo pipefail

source scripts/shared.sh

parse_std_args "$@"

aws ecr get-login-password --region ${aws_region} \
    | docker login \
        --password-stdin \
        --username AWS \
        "${aws_account}.dkr.ecr.${aws_region}.amazonaws.com/${repository}"

aws ecr describe-repositories --repository-names $repository > /dev/null 2>&1


if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name $repository > /dev/null
fi

docker tag $repository:$full_version-$device $aws_account.dkr.ecr.$aws_region.amazonaws.com/$repository:$full_version-$device
docker tag $repository:$full_version-$device $aws_account.dkr.ecr.$aws_region.amazonaws.com/$repository:$short_version-$device
docker push $aws_account.dkr.ecr.$aws_region.amazonaws.com/$repository:$full_version-$device
docker push $aws_account.dkr.ecr.$aws_region.amazonaws.com/$repository:$short_version-$device
docker logout https://$aws_account.dkr.ecr.$aws_region.amazonaws.com
