# ReadTheDocs version warning MkDocs plugin

"ReadTheDocs version warning MkDocs plugin" is a very basic [mkdocs plugin](http://www.mkdocs.org/user-guide/plugins/)
that replace placeholder text (`### VERSION-WARNING-BANNER-PLACEHOLDER ###`) in the theme template with warning admonition.

## Configuration

```yaml
plugins:
    - readthedocs-version-warning:
        project_id: "000000"
        show_on_versions:
            - latest
```

`project_id` - Id of the target project on ReadTheDocs.
From this project will be used the default version to render link to the stable version.
`show_on_versions` - List of versions on which the banner should appear.