WEEK 11: Resolving the Footer Issue and Addressing Sphinx Warnings

.. post:: August 15, 2024
   :author: Wachiou BOURAIMA
   :tags: google
   :category: gsoc

Hello everyone,
Welcome to the update for Week 11 of my Google Summer of Code (GSoC) 2024 journey. This week, I focused on finalizing the footer issue on the FURY website and tackling some Sphinx warnings related to attribute and property naming conflicts. Here’s a detailed look at what I accomplished and the challenges faced.


Fixing the Footer Issue
------------------------

In the previous week, I identified the root cause of the footer deformation. The problem arose when hovering over elements, which caused their size to increase, thereby affecting the padding of their container and subsequently the entire footer layout.
To illustrate the issue and the resolution, I have included the following videos:

Before Fixing the Footer Issue:
Video demonstrating the footer deformation before the fix.

.. raw:: html

    <iframe src="" width="640" height="390" frameborder="0" allowfullscreen></iframe>


After Fixing the Footer Issue:
Video showing the footer after applying the fix.

.. raw:: html

    <iframe src="" width="640" height="390" frameborder="0" allowfullscreen></iframe>

To address this, I experimented with different approaches. Initially, I tried adjusting the font-size of the elements on hover by making them bold instead. This resolved the deformation issue but did not align with the design specifications of the homepage footer.

After reconsidering, I added some properties to the .class-columns in the styles.css file to better adapt the footer style and prevent any layout issues. This approach aimed to maintain the design integrity while addressing the layout problem effectively.


Handling Sphinx Warnings
------------------------

In addition to fixing the footer, I worked on resolving warnings caused by Sphinx due to naming conflicts between attributes and properties. To mitigate these warnings, I initially added :no-index: directives in the .rst files for functions and classes to prevent indexing issues.
However, during our weekly meeting with my mentor, it became clear that this solution might hinder the indexing and referencing of functions, modules, and classes on the FURY site and the web. Therefore, I need to re-evaluate the issue and find a more suitable solution that ensures proper indexing while addressing the warnings.


What’s Next ?
-------------

For the upcoming week, I plan to:
- Delve deeper into the Sphinx warnings related to attribute and property naming conflicts to develop a more appropriate solution.
- Continue to refine the footer styling to ensure it meets design specifications while maintaining functionality.

Thank you for following my progress. I look forward to sharing further updates and solutions in the coming weeks!