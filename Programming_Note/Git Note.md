Git速查笔记

[教程链接及各位大佬笔记](https://github.com/michaelliao/learngit)

新建仓库：

`git init`

添加文件

`git add readme.txt`

提交更改

`git commit -m 'add readme.txt'`	

查看状态

`git status`

查看提交日志

`git log`
`git log --pretty=oneline`

查看当前文件与上次保存源文件区别

`git diff readme.txt`

回退到上一个版本

`git reset --hard HEAD^   //HEAD^是上一个版本，HEAD~100是上一百个版本`

查找每一次命令历史，假设查到commit id是ec4ac06 

`git reflog`

`git reset --hard ec4ac06 `

恢复文件

`git checkout -- readme.txt  #用版本库里的版本替换工作区的版本`

关联远程库并把远程库命名为origin

`git remote add origin git@server-name:path/repo-name.git`

查看远程库信息

`git remote -v`

推动master分支内容到远程库

`git push origin master`

从远程库中下载代码到本地

`git clone git@github.com:michaelliao/gitskills.git`

创建dev分支并切换至dev分支

`git checkout -b dev`

`git switch -c dev`

查看当前分支

`git branch`

切换到master分支

`git checkout master`

`git switch master`

现处于master分支，将dev的分支合并至master

`git merge dev`

删除dev分支

`git branch -d dev`

多人协作时通常只有master分支，在本地创建和远程分支对应的分支branch-name

`git checkout -b branch-name origin/branch-name`

修复bug时，我们会通过创建新的bug分支进行修复，然后合并，最后删除；

当手头工作没有完成时，先把工作现场`git stash`一下，然后去修复bug，修复后，再`git stash pop`，回到工作现场；

在master分支上修复的bug，想要合并到当前dev分支，可以用`git cherry-pick <commit id>`命令，把bug提交的修改“复制”到当前分支，避免重复劳动。

抓取远程的新提交`git pull`



`git tag v1.0  #给最新的commit打标签v1.0`

`git tag <tagname> <commit-id>   #给指定的commit-id打上tagname标签`

`git tag -d v1.0   #删除tag`

`git push origin <tagname> #将本地tagname推送到远程服务器`



Git概念

工作区（Working Directory）：文件夹

版本库（Repository）：.git文件夹，其中有暂存区stage，自动创建首个分支master，及指向master的HEAD指针

暂存区(stage)：git add将文件从工作区移动至暂存区，待提交的文件修改通通放到暂存区，git commit将暂存区所有内容提交至当前分支

标签: 版本库的快照，就是指向某个commit的不可变的指针，跟某个commit绑定在一起