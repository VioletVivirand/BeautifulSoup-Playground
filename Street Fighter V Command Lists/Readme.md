用來爬 http://streetfighter.com/ 網站裡，所有角色招式表的 Code。

特殊符號會用 `{{<` 和 `>}}` 包裝起來，為的是符合 [Go Lang](https://golang.org) 的 Template Syntax，因為我想要玩 [Hugo](http://gohugo.io)。

之後可以配合 [Shortcodes](https://gohugo.io/extras/shortcodes/) 來 Render 吧。